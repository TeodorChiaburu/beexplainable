// Initialize jsPsych
var jsPsych = initJsPsych({
  show_progress_bar: true
});

// Create timeline
var timeline = [];
const protos = ["img/Andrena_bicolor_proto.jpg", "img/Andrena_flavipes_proto.jpg", "img/Andrena_fulva_proto.jpg",
				        "img/Bombus_hortorum_proto.jpg", "img/Bombus_lucorum_proto.jpg", "img/Bombus_pratorum_proto.jpg"];
const test_samples = ["img/Andrena_bicolor_40186737_3.jpg",
                      "img/Andrena_flavipes_5795371_2.jpg",
                      "img/Andrena_fulva_24881697_4.jpg",
                      "img/Bombus_hortorum_7236392_1.jpg",
                      "img/Bombus_terrestris_48053523_1.jpg",
                      "img/Bombus_pratorum_20908187_1.jpg",

                      "img/Andrena_bicolor_39411385_1.jpg",
                      "img/Andrena_fulva_11872393_2.jpg",
                      "img/Bombus_hortorum_84214007_3.jpg",
                      "img/Bombus_terrestris_48213526_1.jpg",
                      "img/Bombus_pratorum_21985654_1.jpg",

                      "img/Andrena_bicolor_39748872_5.jpg",
                      "img/Andrena_flavipes_68809988_2.jpg",
                      "img/Bombus_hortorum_8829930_3.jpg",
                      "img/Bombus_terrestris_68122824_2.jpg",
                      "img/Bombus_pratorum_21985654_5.jpg",

                      "img/Andrena_bicolor_39748872_3.jpg",
                      "img/Andrena_flavipes_56925373_1.jpg",
                      "img/Andrena_fulva_12231414_3.jpg",
                      "img/Bombus_hortorum_91137042_2.jpg",
                      "img/Bombus_terrestris_55479040_5.jpg",
                      "img/Bombus_pratorum_21992207_1.jpg"
                      ];

const exps = ["img/Andrena_bicolor_40186737_3_clsok_conok.jpg",
              "img/Andrena_flavipes_5795371_2_clsok_conok.jpg",
              "img/Andrena_fulva_24881697_4_clsok_conok.jpg",
              "img/Bombus_hortorum_7236392_1_clsok_conok.jpg",
              "img/Bombus_terrestris_48053523_1_clsok_conok.jpg",
              "img/Bombus_pratorum_20908187_1_clsok_conok.jpg",

              "img/Andrena_bicolor_39411385_1_clsok_conno.jpg",
              "img/Andrena_fulva_11872393_2_clsok_conno.jpg",
              "img/Bombus_hortorum_84214007_3_clsok_conno.jpg",
              "img/Bombus_terrestris_48213526_1_clsok_conno.jpg",
              "img/Bombus_pratorum_21985654_1_clsok_conno.jpg",

              "img/Andrena_bicolor_39748872_5_clsno_conok.jpg",
              "img/Andrena_flavipes_68809988_2_clsno_conok.jpg",
              "img/Bombus_hortorum_8829930_3_clsno_conok.jpg",
              "img/Bombus_terrestris_68122824_2_clsno_conok.jpg",
              "img/Bombus_pratorum_21985654_5_clsno_conok.jpg",

              "img/Andrena_bicolor_39748872_3_clsno_conno.jpg",
              "img/Andrena_flavipes_56925373_1_clsno_conno.jpg",
              "img/Andrena_fulva_12231414_3_clsno_conno.jpg",
              "img/Bombus_hortorum_91137042_2_clsno_conno.jpg",
              "img/Bombus_terrestris_55479040_5_clsno_conno.jpg",
              "img/Bombus_pratorum_21992207_1_clsno_conno.jpg"
              ];
const true_labels = ["Andrena bicolor", "Andrena flavipes", "Andrena fulva", "Bombus hortorum", "Bombus lucorum", "Bombus pratorum",
                     "Andrena bicolor",                     "Andrena fulva", "Bombus hortorum", "Bombus lucorum", "Bombus pratorum",
                     "Andrena bicolor", "Andrena flavipes",                  "Bombus hortorum", "Bombus lucorum", "Bombus pratorum",
                     "Andrena bicolor", "Andrena flavipes", "Andrena fulva", "Bombus hortorum", "Bombus lucorum", "Bombus pratorum"];
const classes = ["Andrena bicolor", "Andrena flavipes", "Andrena fulva", "Bombus hortorum", "Bombus lucorum", "Bombus pratorum"];

// Grid with protos (just labels beneath, no buttons)
var proto_grid = `
      <div id="div_row">
          <div class="row">
              <div class="column">
                  <div class="card">
                      <img src="img/Andrena_bicolor_proto.jpg" alt="bico">
                      <h5>Andrena bicolor</h5>
                  </div>
              </div>

              <div class="column">
                  <div class="card">
                      <img src="img/Andrena_flavipes_proto.jpg" alt="flavi">
                      <h5>Andrena flavipes</h5>
                  </div>
              </div>

              <div class="column">
                  <div class="card">
                      <img src="img/Andrena_fulva_proto.jpg" alt="fulva">
                      <h5>Andrena fulva</h5>
                  </div>
              </div>

          </div>

          <div class="row">
              <div class="column">
                  <div class="card">
                      <img src="img/Bombus_hortorum_proto.jpg" alt="hort">
                      <h5>Bombus hortorum</h5>
                  </div>
              </div>

              <div class="column">
                  <div class="card">
                      <img src="img/Bombus_lucorum_proto.jpg" alt="luco">
                      <h5>Bombus lucorum</h5>
                  </div>
              </div>

              <div class="column">
                  <div class="card">
                      <img src="img/Bombus_pratorum_proto.jpg" alt="prato">
                      <h5>Bombus pratorum</h5>
                  </div>
              </div>
          </div>
	</div>
	`;

// Preload images
var preload = {
    type: jsPsychPreload,
    images: [protos,
             test_samples,
             exps]
};
timeline.push(preload);

// Define welcome message trial
var welcome = {
    type: jsPsychHtmlButtonResponse,
    stimulus: `<strong>Welcome to the <i>beexplainable</i> experiment!</strong>
               <p><i>Note</i>: Please only do this experiment <strong>once</strong>.</p>`,
    choices: ['Continue']
};
timeline.push(welcome);

// Define instructions trial
var instructions = {
    type: jsPsychHtmlButtonResponse,
    stimulus: `	  
      <p>In this experiment, you will be shown images of 6 
	wild bee species and be asked to solve two tasks.</p><p><strong>Task 1</strong>: Assign a class to the
	test image based on the prototypes shown on the right half of the page.</p>
      <p><strong>Task 2</strong>: Assign a class while knowing
	our model's prediction and seeing an explanation for it.</p>
	    <p>After these tasks, you will be asked to rate several statements regarding your experience 
	throughout the experiment.</p>
	    <p><i>Note</i>: From this moment on, please avoid resizing your browser window, as this may cause 
	    the zooming tool to malfunction.</p>
    `,
    choices: ['Continue']
};
timeline.push(instructions);

// Show user prototypes for the first time before starting tasks
var just_protos = {
    type: jsPsychHtmlButtonResponse,
    stimulus:
      proto_grid +
      `<div id="just_protos_prompt_div"><p>Before starting the experiment, take your time and look at the 6 samples on the right.
	Each of them was chosen as a prototype of their class. Throughout the whole experiment
	you will be shown these representative samples next to the test samples to help you
	decide which class the test sample belongs to.</p>
	<p>Whenever you are ready, click <strong>Continue</strong> to start the first task:</p>
	<p><strong>Task 1: Assign a class to the
	test image based on the prototypes.</strong></p></div>`,
    choices: ['Continue'],
    post_trial_gap: 1000
};
timeline.push(just_protos);

// Define trial stimuli array for timeline variables
var test_stimuli = [];
for (let i = 0; i < test_samples.length; i++) {
  test_stimuli.push({stimulus: test_samples[i], correct_response: true_labels[i]});
};

var exp_stimuli = [];
for (let i = 0; i < exps.length; i++) {
  exp_stimuli.push({stimulus: exps[i], correct_response: true_labels[i]});
};

// Define fixation
var fixation = {
    type: jsPsychHtmlKeyboardResponse,
    stimulus: '<div style="font-size:60px;">+</div>',
    choices: "NO_KEYS",
    trial_duration: function(){
      return jsPsych.randomization.sampleWithoutReplacement([250, 500, 750], 1)[0]; // = how long to wait till next test sample is shown
    },
    data: {
      task: 'fixation'
    }
};

/*** WITHOUT MODEL ***/

var test_no_model = {
    type: jsPsychImageButtonResponse,
    stimulus: jsPsych.timelineVariable('stimulus'),
    choices: classes, // Also the button labels
    data: {
      task: 'response',
      correct_response: jsPsych.timelineVariable('correct_response')
    },
    on_finish: function(data){
      // Note: Class indices are compared, not labels
      data.correct = jsPsych.pluginAPI.compareKeys(classes[data.response], data.correct_response);
    }
};

var test_procedure_no_model = {
    timeline: [fixation, test_no_model],
    timeline_variables: test_stimuli,
    repetitions: 1,
    randomize_order: true
};
timeline.push(test_procedure_no_model);

var debrief_block_no_model = {
    type: jsPsychHtmlButtonResponse,
    stimulus: function() {

      var trials = jsPsych.data.get().filter({task: 'response'});
      var correct_trials = trials.filter({correct: true});
      var accuracy = Math.round(correct_trials.count() / trials.count() * 100);
      var rt = Math.round(trials.select('rt').mean());

      return `<p>Num. trials: ${trials.count()}, out of which ${correct_trials.count()} were correct.</p>
	      <p>You responded correctly on ${accuracy}% of the trials.</p>
        <p>Your average response time was ${rt}ms.</p>
        <p>Click <strong>Continue</strong> to start the next task:</p>
        <p><strong>Task 2: Assign a class while knowing our model's prediction and seeing an explanation for it.</strong></p>`;
    },
    choices: ['Continue']
};
timeline.push(debrief_block_no_model);

/*** WITH EXPLANATIONS ***/

var test_with_exp = {
    type: jsPsychImageButtonResponse,
    stimulus: jsPsych.timelineVariable('stimulus'),
    choices: classes,
    data: {
      task: 'response_exp',
      correct_response: jsPsych.timelineVariable('correct_response')
    },
    on_finish: function(data){
      data.correct = jsPsych.pluginAPI.compareKeys(classes[data.response], data.correct_response);
    }
};

var test_procedure_with_exp = {
    timeline: [fixation, test_with_exp],
    timeline_variables: exp_stimuli,
    repetitions: 1,
    randomize_order: true
};
timeline.push(test_procedure_with_exp);

var debrief_block_with_exp = {
    type: jsPsychHtmlButtonResponse,
    stimulus: function() {

      var trials = jsPsych.data.get().filter({task: 'response_exp'});
      var correct_trials = trials.filter({correct: true});
      var accuracy = Math.round(correct_trials.count() / trials.count() * 100);
      var rt = Math.round(trials.select('rt').mean());

      return `<p>Num. trials: ${trials.count()}, out of which ${correct_trials.count()} were correct.</p>
	      <p>You responded correctly on ${accuracy}% of the trials.</p>
        <p>Your average response time was ${rt}ms.</p>
        <p>Click <strong>Continue</strong> to start the questionnaire. Thank you!</p>`;
    },
    choices: ['Continue']
};
timeline.push(debrief_block_with_exp);

/*** QUESTIONNAIRE ***/

var questionnaire = {
  type: jsPsychSurveyMultiChoice,
  questions:
  [
      {
        prompt: "1) I did not need support to understand the explanations.",
        name: 'support_exp',
        options: ['strongly disagree', 'somewhat disagree', 'neutral', 'somewhat agree', 'strongly agree'],
        required: true,
        horizontal: true
      },
      {
        prompt: "2) I found the explanations helped me to understand causality.",
        name: 'causal_exp',
        options: ['strongly disagree', 'somewhat disagree', 'neutral', 'somewhat agree', 'strongly agree'],
        required: true,
        horizontal: true
      },
      {
        prompt: "3) I was able to use the explanations with my knowledge base.",
        name: 'know_exp',
        options: ['strongly disagree', 'somewhat disagree', 'neutral', 'somewhat agree', 'strongly agree'],
        required: true,
        horizontal: true
      },
      {
        prompt: "4) I think that most people would learn to understand the explanations very quickly.",
        name: 'understand_exp',
        options: ['strongly disagree', 'somewhat disagree', 'neutral', 'somewhat agree', 'strongly agree'],
        required: true,
        horizontal: true
      }
  ],
  choices: ['Continue']
};
timeline.push(questionnaire);

// Define goodbye message trial
var goodbye = {
    type: jsPsychHtmlButtonResponse,
    stimulus: "<strong>Thank you for participating! Have a nice day :^)</strong>",
    choices: ['Finish']
};
timeline.push(goodbye);

// Start the experiment
jsPsych.run(timeline);