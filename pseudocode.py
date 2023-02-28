"""
Basic idea of jsPsych : the timeline
(similar to 0_hello_world.html and 1_beginner.html)
"""

import jspsych


jsPsychObject = jspsych.initialize()

timeline = [] # Initialize a timeline (list of events for the experiment)

trial_0 = {
    'type': 'imageButtonResponse', # Specify type of trial
    'stimulus': 'hot_dogs/img00.png',
    'choices': ['hot dogs', 'legs'],
    'prompt': 'Did the image contain hot dogs or legs?',
    'stimulus_duration': 750, # Show image for 750ms before it disappears
}
timeline.append(trial_0)

trial_1 = {
    'type': 'imageButtonResponse', # Specify type of trial
    'stimulus': 'legs/img00.png',
    'choices': ['hot dogs', 'legs'],
    'prompt': 'Did the image contain hot dogs or legs?',
    'stimulus_duration': 750, # Show image for 750ms before it disappears
}
timeline.append(trial_1)

jsPsychObject.run(timeline) # Run the timeline



"""
Saving data and using nested timelines + timeline variables
(similar to 2_intermediate.html and 3_advanced.html)
"""

import jspsych
import jspsych.preload
import jspsych.keyboardResponse
import jspsych.imageButtonResponse # Separately import each plugin you will use
import jspsych.categorizeImage     # (remember this is on a wesbite so minimizing
import jspsych.freeSortImages      #  stuff to import makes the page load faster)

from util import write_data_to_server


def function_to_evaluate_when_experiment_ends():
    jsPsychObject.print_out_data() # Somewhat confusing: jsPsychObject is a global variable
    write_data_to_server() # <-- this function uses `url_php_script` and `output_filename`

# Initialize the jsPsychObject with settings to save data
settings = {
    'on_finish': function_to_evaluate_when_experiment_ends,
    'on_data_update': write_data_to_server,
    'show_progress_bar': True
}
jsPsychObject = jspsych.initialize(settings)

# Define some global variables that the `write_data_to_server` function expects
url_php_script = 'https://msaddler.scripts.mit.edu/jspsych_tutorial_960/write_data.php'
output_filename = 'data/mydata.json'

timeline = []

variables_for_the_inner_timeline = [
    {'image_path': 'hot_dogs/img00.png', 'correct_response': 0, 'duration': 500},
    {'image_path': 'hot_dogs/img01.png', 'correct_response': 0, 'duration': 500},
    {'image_path': 'hot_dogs/img02.png', 'correct_response': 0, 'duration': 500},
    # ...
    {'image_path': 'legs/img00.png', 'correct_response': 1, 'duration': 500},
    {'image_path': 'legs/img01.png', 'correct_response': 1, 'duration': 500},
    {'image_path': 'legs/img02.png', 'correct_response': 1, 'duration': 500},
    # ...
]
inner_timeline = [
    {
        'type': 'jsPsychCategorizeImage',
        'stimulus': jsPsychObject.get_variable('image'),
        'prompt': "Press the `0` key for hot dogs or the `1` key for legs",
        'choices': ['0', '1'],
        'key_answer': jsPsychObject.get_variable('correct_response'),
        'stimulus_duration': jsPsychObject.get_variable('duration'),
        # ...
    }
]
trials = {
    'timeline': inner_timeline,
    'timeline_variables': variables_for_the_inner_timeline,
    'randomize_order': True
}
timeline.append(trials)

jsPsychObject.run(timeline)
