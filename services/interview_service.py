import random
from datetime import datetime
from database.db import db
from models.interview import Interview, Question, Answer, AIFeedback
from services.question_bank import QUESTION_BANK
from services.gemini_service import GeminiService

class InterviewService:
    @staticmethod
    def create_interview(user_id, role, difficulty, interview_type, count=5, use_ai=True):
        """
        Generates a new interview record populated with non-repeating questions
        selected from Gemini AI or question bank.
        """
        count = int(count)
        selected_questions = []

        # Attempt AI question generation
        if use_ai:
            ai_questions = GeminiService.generate_ai_questions(role, difficulty, count, interview_type)
            if ai_questions and len(ai_questions) > 0:
                selected_questions = ai_questions

        # Fallback to question bank if AI returns empty
        if not selected_questions:
            filtered = []
            for q in QUESTION_BANK:
                type_match = (interview_type == "Mixed") or (q["type"] == interview_type)
                role_match = (q["role"] == role) or (q["role"] == "All Roles")
                diff_match = (q["difficulty"] == difficulty)
                if type_match and role_match and diff_match:
                    filtered.append(q)

            if len(filtered) < count:
                for q in QUESTION_BANK:
                    if q not in filtered:
                        type_match = (interview_type == "Mixed") or (q["type"] == interview_type)
                        role_match = (q["role"] == role) or (q["role"] == "All Roles")
                        if type_match and role_match:
                            filtered.append(q)

            if len(filtered) < count:
                for q in QUESTION_BANK:
                    if q not in filtered:
                        filtered.append(q)

            sampled = random.sample(filtered, min(count, len(filtered)))
            selected_questions = [{
                "question": q["question"],
                "topic": q["topic"],
                "difficulty": difficulty,
                "sample_answer": q["sample_answer"]
            } for q in sampled]

        # Instantiate Interview Record
        interview = Interview(
            user_id=user_id,
            role=role,
            difficulty=difficulty,
            interview_type=interview_type,
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
