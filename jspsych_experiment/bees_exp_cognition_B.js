// Initialize jsPsych
var jsPsych = initJsPsych({
  show_progress_bar: true
});

// Create timeline
var timeline = [];
const protos = ["img/Andrena_bicolor_proto.jpg", "img/Andrena_flavipes_proto.jpg", "img/Andrena_fulva_proto.jpg",
				        "img/Bombus_hortorum_proto.jpg", "img/Bombus_lucorum_proto.jpg", "img/Bombus_pratorum_proto.jpg"];

// The 6 possible classes
// Note: also used as label vector for Task 2
const classes = ["Andrena bicolor", "Andrena flavipes", "Andrena fulva", "Bombus hortorum", "Bombus lucorum", "Bombus pratorum"];

const test_samples   = ["img/Andrena_bicolor_39411385_1.jpg",
                        "img/Andrena_flavipes_56925373_1.jpg",
                        "img/Andrena_fulva_24881697_4.jpg",
                        "img/Bombus_hortorum_7236392_1.jpg",
                        "img/Bombus_terrestris_48053523_1.jpg",
                        "img/Bombus_pratorum_20908187_1.jpg",
                        "img/Andrena_bicolor_39748872_3.jpg",
                        "img/Andrena_flavipes_68809988_2.jpg",
                        "img/Andrena_fulva_12231414_3.jpg",
                        "img/Bombus_hortorum_84214007_3.jpg",
                        "img/Bombus_terrestris_48213526_1.jpg",
                        "img/Bombus_pratorum_21985654_1.jpg"
                       ];

// Shuffle indexes for test samples in Tasks 1 and 3
inds = Object.keys(test_samples);
for (let i = inds.length - 1; i > 0; i--) {
  const j = Math.floor(Math.random() * (i + 1));
  [inds[i], inds[j]] = [inds[j], inds[i]];

}

// Shuffle test smaples and labels for Tasks 1 and 3
const test_samples_1 = [];
const labels_1 = [];
const test_samples_2 = [];
const labels_2 = [];
for (let i = 0; i < 6; i++) {
  test_samples_1.push(test_samples[parseInt(inds[i])]);
  labels_1.push(classes[parseInt(inds[i]) % 6]); // test_samples are sorted according to classes vector i.e. the 2nd and the 8th samples will be A. flavipes
}
for (let i = 6; i < 12; i++) {
  test_samples_2.push(test_samples[parseInt(inds[i])]);
  labels_2.push(classes[parseInt(inds[i]) % 6]);
}

const pred_samples = ["img/Andrena_bicolor_40186737_3.jpg",   // ok-ok
                      "img/Andrena_flavipes_5795371_2.jpg",   // ok-ok
                      "img/Andrena_fulva_11872393_2.jpg",     // ok-no
                      "img/Bombus_hortorum_8829930_3.jpg",    // no-ok
                      "img/Bombus_terrestris_68122824_2.jpg", // no-ok
                      "img/Bombus_pratorum_21992207_1.jpg"    // no-no
                     ];
// Model's class predictions for pred_samples
const preds = ["Andrena bicolor", "Andrena flavipes", "Andrena fulva", "Bombus pratorum", "Bombus hortorum", "Bombus lucorum"];

// Model's concept predictions for pred_samples
const natural_exps = ['it is fuzzy dark orange', 'it has fuzzy yellow and black stripes', 'it has a smooth shiny dark brown texture']
const exps = [natural_exps[0] + ' and ' + natural_exps[2],
              natural_exps[2],
              natural_exps[0] + ' and ' + natural_exps[2],
              natural_exps[1],
              natural_exps[1],
              natural_exps[1]];

// Grid with protos (just labels beneath, no buttons)
var proto_grid = `
      <div id="div_row">
          <div id="div_venn" class="row">
              <img src="img/venn_captions.jpg" alt="venn">
          </div>
          
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
             test_samples_1,
             pred_samples,
             test_samples_2]
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
      <p>In this experiment, you will be shown 18 images of 6 
	wild bee species and be asked to solve three tasks.</p><p><strong>Task 1 (6 images)</strong>: Assign a species to the
	test image based on the prototypes shown on the right half of the page.</p>
      <p><strong>Task 2 (6 images)</strong>: Assign a species while also knowing
	our model's prediction and seeing an explanation for it.</p>
	    <p><strong>Task 3 (6 images)</strong>: Assign again a species only with the help of the prototypes 
	    (no model prediction revealed).</p>
	    <p>After these tasks, you will be asked to rate 4 statements regarding your experience 
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
	Each of them was chosen as a prototype of their species. The Venn diagram on the top explains how you can distinguish 
	these 6 species based on three simple visual concepts. Note that <i>B. hortorum</i> has <b>three</b> yellow stripes on its back, 
	while <i>B. lucorum</i> only has <b>two</b>. Throughout the whole experiment you will be shown these representative samples 
	next to the test samples to help you decide which species the test sample belongs to. 
	The Venn diagram will <b>not</b> be shown again.</p><br>
	<p>Whenever you are ready, click <strong>Continue</strong> to start the first task:</p>
	<p><strong>Task 1 (6 images): Assign a species to the
	test image based on the prototypes.</strong></p></div>`,
    choices: ['Continue'],
    post_trial_gap: 1000
};
timeline.push(just_protos);

// Define trial stimuli array for timeline variables
var test_stimuli_1 = [];
for (let i = 0; i < test_samples_1.length; i++) {
  test_stimuli_1.push({stimulus: test_samples_1[i], correct_response: labels_1[i]});
};

var pred_stimuli = [];
for (let i = 0; i < pred_samples.length; i++) {
  pred_stimuli.push({stimulus: pred_samples[i], correct_response: classes[i],
                     pred_class: preds[i], pred_concept: exps[i]});
};

var test_stimuli_2 = [];
for (let i = 0; i < test_samples_2.length; i++) {
  test_stimuli_2.push({stimulus: test_samples_2[i], correct_response: labels_2[i]});
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

/*** WITHOUT MODEL (1) ***/

var test_no_model_1 = {
    type: jsPsychImageButtonResponse,
    stimulus: jsPsych.timelineVariable('stimulus'),
    choices: classes, // Also the button labels
    data: {
      task: 'response_1',
      correct_response: jsPsych.timelineVariable('correct_response')
    },
    on_finish: function(data){
      // Note: Class indices are compared, not labels
      data.correct = jsPsych.pluginAPI.compareKeys(classes[data.response], data.correct_response);
    }
};

var test_procedure_no_model_1 = {
    timeline: [fixation, test_no_model_1],
    timeline_variables: test_stimuli_1,
    repetitions: 1,
    randomize_order: true
};
timeline.push(test_procedure_no_model_1);

var debrief_block_no_model_1 = {
    type: jsPsychHtmlButtonResponse,
    stimulus: function() {

      var trials = jsPsych.data.get().filter({task: 'response_1'});
      var correct_trials = trials.filter({correct: true});
      var accuracy = Math.round(correct_trials.count() / trials.count() * 100);
      var rt = Math.round(trials.select('rt').mean());

      return `<p>Num. trials: ${trials.count()}, out of which ${correct_trials.count()} were correct.</p>
	      <p>You responded correctly on ${accuracy}% of the trials.</p>
        <p>Your average response time was ${rt}ms.</p>
        <p>Click <strong>Continue</strong> to start the next task:</p>
        <p><strong>Task 2 (6 images): Assign a species while also knowing our model's prediction and seeing an explanation for it.</strong></p>`;
    },
    choices: ['Continue']
};
timeline.push(debrief_block_no_model_1);

/*** WITH PREDICTIONS ***/

var test_with_pred = {
    type: jsPsychImageButtonResponse,
    stimulus: jsPsych.timelineVariable('stimulus'),
    choices: classes,
    data: {
      task: 'response_pred',
      correct_response: jsPsych.timelineVariable('correct_response'),
      pred_class: jsPsych.timelineVariable('pred_class'),
      pred_concept: jsPsych.timelineVariable('pred_concept')
    },
    on_finish: function(data){
      data.correct = jsPsych.pluginAPI.compareKeys(classes[data.response], data.correct_response);
    }
};

var test_procedure_with_pred = {
    timeline: [fixation, test_with_pred],
    timeline_variables: pred_stimuli,
    repetitions: 1,
    randomize_order: true
};
timeline.push(test_procedure_with_pred);

var debrief_block_with_pred = {
    type: jsPsychHtmlButtonResponse,
    stimulus: function() {

      var trials = jsPsych.data.get().filter({task: 'response_pred'});
      var correct_trials = trials.filter({correct: true});
      var accuracy = Math.round(correct_trials.count() / trials.count() * 100);
      var rt = Math.round(trials.select('rt').mean());

      return `<p>Num. trials: ${trials.count()}, out of which ${correct_trials.count()} were correct.</p>
	      <p>You responded correctly on ${accuracy}% of the trials.</p>
        <p>Your average response time was ${rt}ms.</p>
        <p>Click <strong>Continue</strong> to start the next task:</p>
        <p><strong>Task 3 (6 images): Assign again a species only with the help of the prototypes 
	    (no model prediction revealed).</strong></p>`;
    },
    choices: ['Continue']
};
timeline.push(debrief_block_with_pred);

/*** WITHOUT MODEL (2) ***/

var test_no_model_2 = {
    type: jsPsychImageButtonResponse,
    stimulus: jsPsych.timelineVariable('stimulus'),
    choices: classes, // Also the button labels
    data: {
      task: 'response_2',
      correct_response: jsPsych.timelineVariable('correct_response')
    },
    on_finish: function(data){
      // Note: Class indices are compared, not labels
      data.correct = jsPsych.pluginAPI.compareKeys(classes[data.response], data.correct_response);
    }
};

var test_procedure_no_model_2 = {
    timeline: [fixation, test_no_model_2],
    timeline_variables: test_stimuli_2,
    repetitions: 1,
    randomize_order: true
};
timeline.push(test_procedure_no_model_2);

var debrief_block_no_model_2 = {
    type: jsPsychHtmlButtonResponse,
    stimulus: function() {

      var trials = jsPsych.data.get().filter({task: 'response_2'});
      var correct_trials = trials.filter({correct: true});
      var accuracy = Math.round(correct_trials.count() / trials.count() * 100);
      var rt = Math.round(trials.select('rt').mean());

      return `<p>Num. trials: ${trials.count()}, out of which ${correct_trials.count()} were correct.</p>
	      <p>You responded correctly on ${accuracy}% of the trials.</p>
        <p>Your average response time was ${rt}ms.</p>
        <p>Click <strong>Continue</strong> to start the questionnaire.</p>`;
    },
    choices: ['Continue']
};
timeline.push(debrief_block_no_model_2);


/*** QUESTIONNAIRE ***/

var questionnaire = {
  type: jsPsychSurveyMultiChoice,
  questions:
  [
      {
        prompt: "1) I did not need support to understand the model's explanations.",
        name: 'support_exp',
        options: ['strongly disagree', 'somewhat disagree', 'neutral', 'somewhat agree', 'strongly agree'],
        required: true,
        horizontal: true
      },
      {
        prompt: "2) I found the model's explanations helped me to understand causality.",
        name: 'causal_exp',
        options: ['strongly disagree', 'somewhat disagree', 'neutral', 'somewhat agree', 'strongly agree'],
        required: true,
        horizontal: true
      },
      {
        prompt: "3) I was able to use the model's explanations with my knowledge base.",
        name: 'know_exp',
        options: ['strongly disagree', 'somewhat disagree', 'neutral', 'somewhat agree', 'strongly agree'],
        required: true,
        horizontal: true
      },
      {
        prompt: "4) I think that most people would learn to understand the model's explanations very quickly.",
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