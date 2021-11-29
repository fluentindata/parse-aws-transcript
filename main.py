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


def get_all_words_between(start_time, end_time, time_word_map):
    # k: v if you want both time and word
    return [v for k, v in time_word_map.items() if \
            start_time <= k < end_time]


def extract_speaker_segments(speaker_labels, time_word_map):
    speakers = speaker_labels.get('speakers')
    segments = speaker_labels.get('segments')

    list_of_segments_tupled = []

    for segment in segments:
        speaker = segment.get('speaker_label')

        start_time = float(segment.get('start_time'))
        end_time = float(segment.get('end_time'))
        words = get_all_words_between(start_time, end_time, time_word_map)

        list_of_segments_tupled.append((speaker, start_time, words))

    return list_of_segments_tupled


def combine_same_speaker_segments(speaker_segments):
    combined_segments = []
    last_seen_speaker = None
    for speaker, start_time, words in speaker_segments:
        if last_seen_speaker is None or speaker != last_seen_speaker:
            combined_segments.append((speaker, start_time, words))
            last_seen_speaker = speaker

        elif speaker == last_seen_speaker:
            # get last added segment
            old_speaker, old_start_time, old_words = combined_segments[-1]
            old_words.extend(words)
    return combined_segments






if __name__ == '__main__':
    transcript = load_transcript_from_json("aws-transcript.json")
    results = transcript.get('results')
    text = results.get('transcripts')[0].get("transcript")
    speaker_labels = results.get('speaker_labels')
    items = results.get('items')

    # print_low_confidence_words(items, 0.5)
    built_transcript = []
    start_times = []

    time_to_word = {}

    # using to hold state on start_time to add punctuation after-the-fact
    # to the time_to_word map
    start_time = None

    for item in items:
        alternatives = item.get('alternatives')
        if item.get('type') == 'punctuation':
            built_transcript.pop()

        word = alternatives[0].get('content')

        if item.get('type') == 'pronunciation':
            start_time = float(item.get("start_time"))
            start_times.append(start_time)
            time_to_word[start_time] = word
            word = '<span class="word" onclick="svt({})">{}</span>'.format(start_time, word)
        else:
            time_to_word[start_time] = str(time_to_word.get(start_time)) + word
            word = '<span class="punctuation">{}</span>'.format(word)

        built_transcript.append(word)
        built_transcript.append(" ")

        # if len(built_transcript) > 1000:
        #     break

    speaker_segments = extract_speaker_segments(speaker_labels, time_to_word)
    speaker_segments = combine_same_speaker_segments(speaker_segments)

    joined_text = "".join(built_transcript)
    print(joined_text)

    for speaker, start_time, words in speaker_segments:
        print("{}@ {}: {}".format(speaker, start_time, " ".join(words)))

    speaker_annotated_html_paragraphs = []
    for speaker, start_time, words in speaker_segments:
        speaker_annotated_html_paragraphs.append('<h3 class="{}">{} {}</h3> <span class="word" class="word" '
                                                 'onclick="svt({})">{}'.format
                                                 (speaker, speaker, start_time, start_time, " ".join(words)))
    if joined_text == text:
        print("MATCHES")

    print(speaker_annotated_html_paragraphs)

    with open("output.html", 'w') as output:
        output.write(inject_video_player('_OtZ49i-yyk'))
        output.write('<div class="centerpanel">')
        output.write('<script>var video_start_times = {}</script>'.format(start_times))
        output.write("".join(speaker_annotated_html_paragraphs))
        output.write('</div>')

    # for diff in dl.context_diff(joined_text, text):
    #     print(diff)
