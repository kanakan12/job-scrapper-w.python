from flask import Flask, render_template, request, redirect, send_file
from stackoverflow import get_jobs as get_so_jobs
from weworkremotely import get_jobs as get_wr_jobs
from remoteok import get_jobs as get_re_jobs
from save import save_to_file

"""
These are the URLs that will give you remote jobs for the word 'python'

https://stackoverflow.com/jobs?r=true&q=python
https://weworkremotely.com/remote-jobs/search?term=python
https://remoteok.io/remote-dev+python-jobs

Good luck!
"""

app = Flask("Scrapper")

db = {}

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/detail")
def detail():
    try:
        word = request.args.get("word")
        if word:
            word = word.lower()
            existingJobs = db.get(word)
            if existingJobs:
                jobs = existingJobs
            else:
                jobs = get_so_jobs(word) + get_wr_jobs(word) + get_re_jobs(word)
                if jobs:
                    db[word] = jobs
                else:
                    return redirect("/")
        else:
            return redirect("/")
    except:
        return redirect("/")
        
    return render_template("detail.html", count = len(jobs), word = word, jobs = jobs)

@app.route("/export")
def export():
    try:
        word = request.args.get("word")
        if not word:
            raise Exception()
        word = word.lower()
        jobs = db.get(word)
        if not jobs:
            raise Exception()
        save_to_file(jobs, word)
        return send_file(f"jobs-{word}.csv", as_attachment=True)
    except:
        return redirect("/")

app.run()