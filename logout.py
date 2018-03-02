from redirect import redirect
from cookie import disable_cookie, cookie_check
from vial import render_template


#def logout(headers, body, data):
#    cookie = str(headers['http-cookie']).replace('session_id=', '')
#    disable_cookie(cookie)
#    return redirect(headers=headers, body=body, data=data, message='Zostales wylogowany!')


def logout(headers, body, data):
    cookie = str(headers['http-cookie']).replace('sessionid=', '')
    if not cookie_check(cookie):
        return render_template('html/home.html', body=body, data=data, headers=headers,
                               message='Zostales wylogowany!'), 200, {}
    disable_cookie(cookie)
    return render_template('html/redirect.html', body=body, data=data, headers=headers,
                           message='Trwa wylogowywanie...'), 200, {}