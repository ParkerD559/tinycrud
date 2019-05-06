from tinycrud import TinyCRUD

app = TinyCRUD()
app.resource('version', 1)

app.run()
