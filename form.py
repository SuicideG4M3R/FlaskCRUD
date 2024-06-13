from flask import render_template


def check_user(username, email, context):
    if not username or not email:
        context['error'] = 'Username and email are required'
        return render_template('index.html', context=context)

    if not len(username) >= 3:
        context['error'] = 'Username must be at least 3 characters'
        return render_template('index.html', context=context)

    if '@' not in email:
        context['error'] = 'Email must contain @'
        return render_template('index.html', context=context)
