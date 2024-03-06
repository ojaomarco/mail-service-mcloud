from rocketry import Rocketry

app = Rocketry()

@app.task('every 500 ms')
def do_things():
    print('oii')

if __name__ == "__main__":
    app.run()