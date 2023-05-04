from website._init_ import create_app


from flask_qrcode import QRcode

app = create_app()
QRcode(app)

if __name__ == '__main__':
    app.run(debug=True, port=3000)