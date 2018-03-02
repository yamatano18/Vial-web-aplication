from vial import render_template

def redirect(headers, body, data, message='Taka strona nie istnieje!'):
    cookie = str(headers['http-cookie']).replace('sessionid=', '')
    return render_template('html/redirect.html', body=body, data=data, headers=headers, message=message), 200, {'Set-Cookie': cookie}