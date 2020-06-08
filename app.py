from flask import Flask, render_template
from wtforms import SubmitField, TextAreaField
from wtforms.validators import InputRequired
from flask_wtf import FlaskForm
from config import config

from models.text_rank import TextRankSummarizer
from models.lda import LDASummarizer

app = Flask(__name__)
app.config.from_object(config["development"])
text_rank_summarizer = TextRankSummarizer()
lda_summarizer = LDASummarizer()


class InputForm(FlaskForm):
    input_text = TextAreaField("输入文本", validators=[InputRequired(message="请输入有效的文本")])
    submit = SubmitField("提交")


@app.route('/summarize', methods=['GET', 'POST'])
def summarize():
    results = None
    length = None
    form = InputForm()
    # form.input_text.data = app.config["DEFAULT_SUMMARIZED"]
    if form.validate_on_submit():
        results = {}
        content = form.input_text.data
        results['text_rank'] = text_rank_summarizer.summarize(content)
        length = len(results['text_rank'])
        results['lda'] = lda_summarizer.summarize(content)
    
    return render_template('summarize.html', form=form, results=results,
                           length=length)


@app.route('/test', methods=['GET'])
def test():
    return render_template('test.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8000, use_reloader=True)