import json

from html_helpers import inject_video_player


def load_transcript_from_json(transcript_path):
    with open(transcript_path, 'r') as transcript:
        data = json.loads(transcript.read())
        return data


def print_low_confidence_words(items, confidence):
    for item in items:
        if item.get('type') == 'punctuation':
            continue

        alternatives = item.get('alternatives')

        if float(alternatives[0].get('confidence')) < confidence:
            print(item.get('start_time'), alternatives[0].get('content'))


if __name__ == '__main__':
    transcript = load_transcript_from_json("aws-transcript.json")
    results = transcript.get('results')
    text = results.get('transcripts')[0].get("transcript")
    speaker_levels = results.get('speaker_labels')
    items = results.get('items')

    # print_low_confidence_words(items, 0.5)
    built_transcript = []
    start_times = []
    for item in items:
        alternatives = item.get('alternatives')
        if item.get('type') == 'punctuation':
            built_transcript.pop()

        word = alternatives[0].get('content')

        if item.get('type') == 'pronunciation':
            start_time = item.get("start_time");
            start_times.append(float(start_time));
            word = '<span class="word" onclick="svt({})">{}</span>'.format(start_time, word);
        else:
            word = '<span class="punctuation">{}</span>'.format(word);

        built_transcript.append(word)
        built_transcript.append(" ")

        # if len(built_transcript) > 1000:
        #     break

    joined_text = "".join(built_transcript)
    print(joined_text)

    if joined_text == text:
        print("MATCHES")

    with open("output.html", 'w') as output:
        output.write(inject_video_player('_OtZ49i-yyk'))
        output.write('<div class="centerpanel">')
        output.write('<script>var video_start_times = {}</script>'.format(start_times))
        output.write(joined_text)
        output.write('</div>')

    # for diff in dl.context_diff(joined_text, text):
    #     print(diff)