import random
from datetime import datetime
from database.db import db
from models.interview import Interview, Question, Answer, AIFeedback
from services.question_bank import QUESTION_BANK
from services.gemini_service import GeminiService

class InterviewService:
    @staticmethod
    def create_interview(user_id, role, difficulty, interview_type, count=5, use_ai=True, mode='text', resume_text=None):
        """
        Generates a new interview record populated with non-repeating questions
        matching the selected role, interview focus, and calibrated difficulty.
        """
        from services.question_bank import get_bank_questions, normalize_role, normalize_focus
        count = int(count)
        norm_role = normalize_role(role)
        norm_focus = normalize_focus(interview_type)
        selected_questions = []

        # 1. Attempt Resume-Tailored generation if resume_text is provided
        if resume_text and len(resume_text.strip()) > 0:
            selected_questions = GeminiService.generate_resume_interview_questions(
                resume_text=resume_text,
                count=count,
                role=norm_role,
                difficulty=difficulty,
                interview_type=norm_focus
            )
        # 2. Otherwise generate role-based AI questions
        elif use_ai:
            selected_questions = GeminiService.generate_ai_questions(
                role=norm_role,
                difficulty=difficulty,
                count=count,
                question_type=norm_focus
            )

        # 3. Fallback to question bank if needed or short
        if not selected_questions or len(selected_questions) < count:
            bank_q = get_bank_questions(norm_role, norm_focus, difficulty, count)
            if not selected_questions:
                selected_questions = bank_q
            else:
                seen_texts = {q["question"].lower() for q in selected_questions}
                for bq in bank_q:
                    if bq["question"].lower() not in seen_texts:
                        seen_texts.add(bq["question"].lower())
                        selected_questions.append(bq)
                    if len(selected_questions) >= count:
                        break

        selected_questions = selected_questions[:count]

        # Role label to persist
        stored_role = f"{norm_role} (Resume Tailored)" if (resume_text and len(resume_text.strip()) > 0) else norm_role

        # Instantiate Interview Record
        interview = Interview(
            user_id=user_id,
            role=stored_role,
            difficulty=difficulty,
            interview_type=norm_focus,
            mode=mode if mode in ['text', 'voice', 'video'] else 'text',
            total_questions=len(selected_questions),
            start_time=datetime.utcnow(),
            status='in_progress',
            score=0.0
        )
        db.session.add(interview)
        db.session.flush()

        # Create Question Entries
        for idx, q_data in enumerate(selected_questions, start=1):
            q_record = Question(
                interview_id=interview.id,
                question_text=q_data["question"],
                topic=q_data.get("topic", "Technical Concept"),
                difficulty=q_data.get("difficulty", difficulty),
                sample_answer=q_data.get("sample_answer", "Model answer placeholder"),
                order_number=idx
            )
            db.session.add(q_record)

        db.session.commit()
        return interview

    @staticmethod
    def get_interview_by_id(interview_id):
        """Retrieve interview by ID."""
        return Interview.query.get(int(interview_id))

    @staticmethod
    def save_answer_and_evaluate(question_id, answer_text, time_taken=0, role="Software Engineer", difficulty="Medium"):
        """
        Saves user answer and runs Gemini AI evaluation, persisting into AIFeedback table.
        """
        question = Question.query.get(int(question_id))
        if not question:
            return None, None

        # 1. Save or update Answer row
        answer = Answer.query.filter_by(question_id=question.id).first()
        if not answer:
            answer = Answer(question_id=question.id)
            db.session.add(answer)

        ans_clean = answer_text.strip() if answer_text else ""
        answer.answer_text = ans_clean
        answer.time_taken = int(time_taken)
        answer.created_at = datetime.utcnow()
        db.session.commit()

        # 2. Run Gemini AI Evaluation
        eval_res = GeminiService.evaluate_answer(
            question_text=question.question_text,
            user_answer=ans_clean,
            role=role,
            difficulty=difficulty
        )

        # 3. Save or update AIFeedback row
        feedback = AIFeedback.query.filter_by(question_id=question.id).first()
        if not feedback:
            feedback = AIFeedback(
                interview_id=question.interview_id,
                question_id=question.id,
                question=question.question_text
            )
            db.session.add(feedback)

        feedback.answer = ans_clean
        feedback.technical_score = float(eval_res.get('technical_score', 0))
        feedback.communication_score = float(eval_res.get('communication_score', 0))
        feedback.confidence_score = float(eval_res.get('confidence_score', 0))
        feedback.grammar_score = float(eval_res.get('grammar_score', 0))
        feedback.relevance_score = float(eval_res.get('relevance_score', 0))
        feedback.overall_score = float(eval_res.get('overall_score', 0))
        
        feedback.strengths = str(eval_res.get('strengths', ''))
        feedback.weaknesses = str(eval_res.get('weaknesses', ''))
        feedback.improved_answer = str(eval_res.get('improved_answer', ''))
        feedback.missing_key_points = str(eval_res.get('missing_key_points', ''))
        feedback.created_at = datetime.utcnow()

        db.session.commit()

        return answer, feedback

    @staticmethod
    def process_turn(interview_id, question_id, answer_text, time_taken=0):
        """
        Executes a complete automated interview turn:
        1. Evaluates candidate answer via Gemini AI and persists feedback.
        2. Adjusts dynamic difficulty and interview stage.
        3. Generates the next context-aware adaptive question referencing candidate response & resume.
        4. Returns structured JSON for the frontend state machine.
        """
        interview = InterviewService.get_interview_by_id(interview_id)
        if not interview:
            return {'status': 'error', 'message': 'Interview not found'}

        question = Question.query.get(int(question_id))
        if not question or question.interview_id != interview.id:
            return {'status': 'error', 'message': 'Invalid question'}

        # 1. Save and evaluate current answer
        answer, feedback = InterviewService.save_answer_and_evaluate(
            question_id=question.id,
            answer_text=answer_text,
            time_taken=time_taken,
            role=interview.role,
            difficulty=interview.difficulty
        )

        current_q_num = question.order_number
        total_q = interview.total_questions

        # 2. Check if final question reached
        if current_q_num >= total_q:
            InterviewService.complete_interview(interview.id)
            return {
                'status': 'success',
                'completed': True,
                'current_q_num': current_q_num,
                'total_questions': total_q,
                'overall_score': feedback.overall_score if feedback else 75.0,
                'feedback': {
                    'overall_score': feedback.overall_score if feedback else 75.0,
                    'technical_score': feedback.technical_score if feedback else 75.0,
                    'communication_score': feedback.communication_score if feedback else 75.0,
                    'confidence_score': feedback.confidence_score if feedback else 75.0,
                    'relevance_score': feedback.relevance_score if feedback else 75.0,
                    'strengths': feedback.strengths if feedback else '',
                    'weaknesses': feedback.weaknesses if feedback else ''
                }
            }

        # 3. Dynamic difficulty progression
        diff_levels = ["Easy", "Medium", "Hard", "Advanced"]
        curr_diff = interview.difficulty
        if curr_diff not in diff_levels:
            curr_diff = "Medium"
        diff_idx = diff_levels.index(curr_diff)

        last_score = feedback.overall_score if feedback else 75.0
        if last_score >= 80 and diff_idx < len(diff_levels) - 1:
            next_diff = diff_levels[diff_idx + 1]
        elif last_score < 55 and diff_idx > 0:
            next_diff = diff_levels[diff_idx - 1]
        else:
            next_diff = curr_diff

        interview.difficulty = next_diff
        db.session.commit()

        # 4. Determine stage progression based on interview_type
        next_q_num = current_q_num + 1
        from services.question_bank import normalize_focus
        norm_focus = normalize_focus(interview.interview_type)

        if norm_focus == "HR Interview":
            stage_map = {
                1: "Background & Motivation",
                2: "Workplace Fit & Communication",
                3: "Feedback & Growth Mindset",
                4: "Career Goals & Alignment",
                5: "Team Values & Culture"
            }
        elif norm_focus == "Behavioral Interview":
            stage_map = {
                1: "Past Project Challenges",
                2: "Adaptability & Shifting Priorities",
                3: "Cross-Functional Collaboration",
                4: "Ownership & Initiative",
                5: "Incident Remediation & Accountability"
            }
        elif norm_focus == "Scenario Based Interview":
            stage_map = {
                1: "Onboarding & Technical Action Plan",
                2: "Live Production Outage Response",
                3: "Timeline vs Quality Trade-offs",
                4: "Distributed Architecture Redesign",
                5: "Third-Party Integration Failures"
            }
        elif norm_focus == "Problem Solving Interview":
            stage_map = {
                1: "Requirement Decomposition",
                2: "Latency Bottleneck Diagnostics",
                3: "Caching & Invalidation Strategy",
                4: "Large-Scale Data Processing",
                5: "Zero-Downtime Refactoring"
            }
        else: # Technical Interview
            stage_map = {
                1: "Technical Background & Core Stack",
                2: "Language & Architectural Principles",
                3: "Deep-Dive Design Trade-offs",
                4: "Diagnostics & Root Cause Analysis",
                5: "Scalability & Resilience Engineering"
            }

        stage_name = stage_map.get(next_q_num, f"Advanced {norm_focus} Exploration")

        # 5. Gather history and candidate resume
        from services.resume_service import ResumeService
        latest_resume = ResumeService.get_latest_user_resume(interview.user_id)
        resume_text = latest_resume.raw_text if latest_resume else ""

        history = []
        for q in interview.questions:
            if q.order_number <= current_q_num:
                history.append({
                    'question': q.question_text,
                    'answer': q.get_user_answer() or '',
                    'score': q.ai_feedback.overall_score if q.ai_feedback else 75.0
                })

        # 6. Generate adaptive next question
        adaptive_data = GeminiService.generate_adaptive_interview_question(
            role=interview.role,
            difficulty=next_diff,
            question_number=next_q_num,
            total_questions=total_q,
            interview_stage=stage_name,
            previous_history=history,
            candidate_profile=resume_text,
            last_answer=answer_text,
            last_score=last_score,
            interview_type=interview.interview_type
        )

        # 7. Update or create the next Question in database
        next_question = Question.query.filter_by(interview_id=interview.id, order_number=next_q_num).first()
        if not next_question:
            next_question = Question(
                interview_id=interview.id,
                question_text=adaptive_data.get('question'),
                topic=adaptive_data.get('topic', stage_name),
                difficulty=next_diff,
                sample_answer=adaptive_data.get('sample_answer', 'Model solution'),
                order_number=next_q_num
            )
            db.session.add(next_question)
        else:
            next_question.question_text = adaptive_data.get('question')
            next_question.topic = adaptive_data.get('topic', stage_name)
            next_question.difficulty = next_diff
            next_question.sample_answer = adaptive_data.get('sample_answer', 'Model solution')

        db.session.commit()

        return {
            'status': 'success',
            'completed': False,
            'current_q_num': next_q_num,
            'total_questions': total_q,
            'transition_phrase': adaptive_data.get('transition_phrase', 'Thank you. Let us proceed to the next question.'),
            'next_question': {
                'id': next_question.id,
                'order_number': next_question.order_number,
                'question_text': next_question.question_text,
                'topic': next_question.topic,
                'difficulty': next_question.difficulty
            },
            'evaluation': {
                'overall_score': feedback.overall_score if feedback else 75.0,
                'technical_score': feedback.technical_score if feedback else 75.0,
                'communication_score': feedback.communication_score if feedback else 75.0,
                'confidence_score': feedback.confidence_score if feedback else 75.0,
                'relevance_score': feedback.relevance_score if feedback else 75.0,
                'strengths': feedback.strengths if feedback else '',
                'weaknesses': feedback.weaknesses if feedback else ''
            }
        }


    @staticmethod
    def complete_interview(interview_id):
        """
        Marks interview as completed and calculates final overall score from AI feedbacks.
        """
        interview = InterviewService.get_interview_by_id(interview_id)
        if not interview:
            return None

        if interview.status != 'completed':
            interview.status = 'completed'
            interview.end_time = datetime.utcnow()

            # Calculate average score from AI feedback rows
            feedbacks = AIFeedback.query.filter_by(interview_id=interview.id).all()
            if feedbacks:
                scores = [fb.overall_score for fb in feedbacks]
                interview.score = round(sum(scores) / len(scores), 1)
            else:
                interview.score = 75.0

            db.session.commit()

        return interview

    @staticmethod
    def get_summary_metrics(interview_id):
        """Generates comprehensive summary metrics and AI feedback section scores."""
        interview = InterviewService.get_interview_by_id(interview_id)
        if not interview:
            return None

        answered = 0
        skipped = 0
        total_time_secs = 0

        for q in interview.questions:
            ans = q.get_user_answer()
            if ans and len(ans.strip()) > 0:
                answered += 1
            else:
                skipped += 1

            if q.answers:
                total_time_secs += q.answers[-1].time_taken

        mins = total_time_secs // 60
        secs = total_time_secs % 60
        time_str = f"{mins}m {secs}s" if mins > 0 else f"{secs}s"

        # Calculate 5 Section Score Averages
        feedbacks = AIFeedback.query.filter_by(interview_id=interview.id).all()
        if feedbacks:
            tech_avg = round(sum(f.technical_score for f in feedbacks) / len(feedbacks), 1)
            comm_avg = round(sum(f.communication_score for f in feedbacks) / len(feedbacks), 1)
            conf_avg = round(sum(f.confidence_score for f in feedbacks) / len(feedbacks), 1)
            gram_avg = round(sum(f.grammar_score for f in feedbacks) / len(feedbacks), 1)
            rel_avg = round(sum(f.relevance_score for f in feedbacks) / len(feedbacks), 1)
            overall_avg = round(sum(f.overall_score for f in feedbacks) / len(feedbacks), 1)
        else:
            tech_avg = comm_avg = conf_avg = gram_avg = rel_avg = overall_avg = interview.score

        # Generate AI Summary Insights
        ai_summary = GeminiService.generate_interview_summary(
            role=interview.role,
            overall_score=overall_avg,
            feedback_list=feedbacks
        )

        return {
            'total_questions': interview.total_questions,
            'answered': answered,
            'skipped': skipped,
            'time_taken': time_str,
            'status': interview.status.replace('_', ' ').capitalize(),
            'score': overall_avg,
            'section_scores': {
                'technical': tech_avg,
                'communication': comm_avg,
                'confidence': conf_avg,
                'grammar': gram_avg,
                'relevance': rel_avg
            },
            'ai_summary': ai_summary
        }

    @staticmethod
    def get_user_dashboard_stats(user_id):
        """Retrieve dynamic user interview statistics for Dashboard and Profile."""
        interviews = Interview.query.filter_by(user_id=user_id, status='completed').all()
        
        total_count = len(interviews)
        if total_count == 0:
            return {
                'total_interviews': 0,
                'average_score': 0,
                'best_score': 0,
                'weekly_hours': '0.0 hrs',
                'recent_activities': []
            }

        scores = [inv.score for inv in interviews]
        avg_score = round(sum(scores) / total_count, 1)
        best_score = round(max(scores), 1)

        total_secs = sum(inv.duration_seconds for inv in interviews)
        weekly_hours = f"{round(total_secs / 3600.0, 1)} hrs"

        recent = Interview.query.filter_by(user_id=user_id).order_by(Interview.start_time.desc()).limit(5).all()
        activities = []
        for inv in recent:
            activities.append({
                'id': inv.id,
                'type': f"{inv.interview_type} Interview",
                'role': inv.role,
                'score': int(inv.score) if inv.status == 'completed' else 0,
                'date': inv.start_time.strftime('%b %d, %Y'),
                'badge': inv.status.replace('_', ' ').capitalize(),
                'color': 'success' if inv.status == 'completed' else 'warning'
            })

        return {
            'total_interviews': total_count,
            'average_score': avg_score,
            'best_score': best_score,
            'weekly_hours': weekly_hours,
            'recent_activities': activities
        }
