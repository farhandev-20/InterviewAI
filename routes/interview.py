from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from services.interview_service import InterviewService
from services.resume_service import ResumeService
from services.gemini_service import GeminiService
from models.interview import Question, AIFeedback

interview_bp = Blueprint('interview', __name__, url_prefix='/interview')

@interview_bp.route('/setup', methods=['GET', 'POST'])
@login_required
def setup():
    latest_resume = ResumeService.get_latest_user_resume(current_user.id)

    if request.method == 'POST':
        role = request.form.get('role', 'Python Developer')
        difficulty = request.form.get('difficulty', 'Medium')
        interview_type = request.form.get('interview_type', 'Technical Interview')
        mode = request.form.get('mode', 'text')
        count = int(request.form.get('count', 5))
        use_resume = True if request.form.get('use_resume') else False

        # Check for uploaded resume when resume-tailoring is requested
        resume_raw_text = None
        if use_resume:
            if latest_resume and latest_resume.raw_text and len(latest_resume.raw_text.strip()) > 0:
                resume_raw_text = latest_resume.raw_text
            else:
                flash('No uploaded resume found. Proceeding with role-based practice questions.', 'info')

        interview = InterviewService.create_interview(
            user_id=current_user.id,
            role=role,
            difficulty=difficulty,
            interview_type=interview_type,
            count=count,
            use_ai=True,
            mode=mode,
            resume_text=resume_raw_text
        )

        flash('AI Interview session initialized! Good luck.', 'success')
        return redirect(url_for('interview.live', interview_id=interview.id, q=1))

    roles = [
        "Python Developer",
        "Frontend Developer",
        "Backend Developer",
        "Full Stack Developer",
        "Java Developer",
        "UI/UX Designer",
        "Data Analyst",
        "Machine Learning Engineer",
        "HR Interview"
    ]
    difficulties = ["Easy", "Medium", "Hard"]
    types = [
        "Technical Interview",
        "HR Interview",
        "Behavioral Interview",
        "Scenario Based Interview",
        "Problem Solving Interview"
    ]
    question_counts = [5, 10, 15, 20]

    return render_template(
        'interview/setup.html',
        roles=roles,
        difficulties=difficulties,
        types=types,
        question_counts=question_counts,
        latest_resume=latest_resume
    )

@interview_bp.route('/<int:interview_id>/live', methods=['GET', 'POST'])
@login_required
def live(interview_id):
    interview = InterviewService.get_interview_by_id(interview_id)
    if not interview or interview.user_id != current_user.id:
        flash('Unauthorized access or interview session not found.', 'danger')
        return redirect(url_for('dashboard.index'))

    if interview.status == 'completed':
        return redirect(url_for('interview.summary', interview_id=interview.id))

    questions = interview.questions
    total_q = len(questions)

    q_num = request.args.get('q', 1, type=int)
    if q_num < 1:
        q_num = 1
    elif q_num > total_q:
        q_num = total_q

    current_question = questions[q_num - 1]

    if request.method == 'POST':
        action = request.form.get('action', 'next')
        answer_text = request.form.get('answer', '')
        time_taken = request.form.get('time_taken', 0, type=int)

        _, feedback = InterviewService.save_answer_and_evaluate(
            question_id=current_question.id,
            answer_text=answer_text,
            time_taken=time_taken,
            role=interview.role,
            difficulty=interview.difficulty
        )

        if action == 'submit' or (action == 'next' and q_num == total_q):
            InterviewService.complete_interview(interview.id)
            flash('AI Interview evaluation complete!', 'success')
            return redirect(url_for('interview.summary', interview_id=interview.id))

        if action == 'prev' and q_num > 1:
            next_q = q_num - 1
        elif action == 'skip' or action == 'next':
            next_q = min(q_num + 1, total_q)
        else:
            next_q = q_num

        return redirect(url_for('interview.live', interview_id=interview.id, q=next_q))

    user_answer = current_question.get_user_answer() or ""
    current_feedback = AIFeedback.query.filter_by(question_id=current_question.id).first()

    return render_template(
        'interview/live.html',
        interview=interview,
        question=current_question,
        q_num=q_num,
        total_q=total_q,
        user_answer=user_answer,
        feedback=current_feedback
    )

@interview_bp.route('/<int:interview_id>/save-answer', methods=['POST'])
@login_required
def save_answer_ajax(interview_id):
    interview = InterviewService.get_interview_by_id(interview_id)
    if not interview or interview.user_id != current_user.id:
        return jsonify({'status': 'error', 'message': 'Unauthorized'}), 403

    data = request.get_json() or {}
    question_id = data.get('question_id')
    answer_text = data.get('answer', '')
    time_taken = data.get('time_taken', 0)

    if question_id:
        _, feedback = InterviewService.save_answer_and_evaluate(
            question_id=question_id,
            answer_text=answer_text,
            time_taken=time_taken,
            role=interview.role,
            difficulty=interview.difficulty
        )
        return jsonify({
            'status': 'success',
            'overall_score': feedback.overall_score if feedback else 0
        })

    return jsonify({'status': 'error', 'message': 'Invalid question ID'}), 400

@interview_bp.route('/<int:interview_id>/turn', methods=['POST'])
@login_required
def process_turn_ajax(interview_id):
    """
    Automated turn processor: Evaluates candidate answer, dynamically adapts difficulty,
    generates next adaptive question, and updates state.
    """
    interview = InterviewService.get_interview_by_id(interview_id)
    if not interview or interview.user_id != current_user.id:
        return jsonify({'status': 'error', 'message': 'Unauthorized'}), 403

    data = request.get_json() or {}
    question_id = data.get('question_id')
    answer_text = data.get('answer', '')
    time_taken = data.get('time_taken', 0)

    if not question_id:
        return jsonify({'status': 'error', 'message': 'Missing question_id'}), 400

    result = InterviewService.process_turn(
        interview_id=interview.id,
        question_id=question_id,
        answer_text=answer_text,
        time_taken=time_taken
    )

    if result.get('completed'):
        result['redirect_url'] = url_for('interview.report', interview_id=interview.id)

    return jsonify(result)


@interview_bp.route('/<int:interview_id>/follow-up', methods=['POST'])
@login_required
def generate_followup(interview_id):
    interview = InterviewService.get_interview_by_id(interview_id)
    if not interview or interview.user_id != current_user.id:
        return jsonify({'status': 'error', 'message': 'Unauthorized'}), 403

    data = request.get_json() or {}
    question_text = data.get('question_text', '')
    user_answer = data.get('answer', '')

    result = GeminiService.generate_followup_question(
        question_text=question_text,
        user_answer=user_answer,
        role=interview.role,
        difficulty=interview.difficulty
    )
    return jsonify({'status': 'success', 'followup': result.get('followup_question'), 'context': result.get('context')})

@interview_bp.route('/<int:interview_id>/summary')
@login_required
def summary(interview_id):
    interview = InterviewService.get_interview_by_id(interview_id)
    if not interview or interview.user_id != current_user.id:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('dashboard.index'))

    metrics = InterviewService.get_summary_metrics(interview.id)
    return render_template('interview/summary.html', interview=interview, metrics=metrics)

@interview_bp.route('/<int:interview_id>/report')
@login_required
def report(interview_id):
    interview = InterviewService.get_interview_by_id(interview_id)
    if not interview or interview.user_id != current_user.id:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('dashboard.index'))

    metrics = InterviewService.get_summary_metrics(interview.id)
    feedbacks = AIFeedback.query.filter_by(interview_id=interview.id).all()
    feedback_map = {fb.question_id: fb for fb in feedbacks}

    return render_template(
        'interview/report.html',
        interview=interview,
        metrics=metrics,
        feedback_map=feedback_map
    )
