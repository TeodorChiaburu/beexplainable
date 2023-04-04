// Initialize jsPsych
var jsPsych = initJsPsych({
  show_progress_bar: true
});

// Randomly pick whether user will be assigned to group A or B
groups = ['A', 'B'];
function choose_group(groups) {
  var index = Math.floor(Math.random() * groups.length);
  return groups[index];
}
assigned_group = choose_group(groups);

// Create timeline
var timeline = [];
const protos = ["img/Andrena_flavipes_proto.jpg", "img/Andrena_fulva_proto.jpg", "img/Bombus_lucorum_proto.jpg"];

// The 3 possible classes
const classes = ["Andrena flavipes", "Andrena fulva", "Bombus lucorum"];

/*** Task 1 and 3 ***/
// Sample pools for Tasks 1 and 3 (only 4 will be randomly picked for each species)
const pool_samples_flavi = ["img/Andrena_flavipes_28862388_1.jpg",
                            "img/Andrena_flavipes_33657115_1.jpg",
                            "img/Andrena_flavipes_35698472_2.jpg",
                            "img/Andrena_flavipes_40178244_1.jpg",
                            "img/Andrena_flavipes_40832925_2.jpg",
                            "img/Andrena_flavipes_40832925_3.jpg",
                            "img/Andrena_flavipes_41163118_3.jpg",
                            "img/Andrena_flavipes_41517541_1.jpg",
                            "img/Andrena_flavipes_41517541_3.jpg",
                            "img/Andrena_flavipes_42347630_1.jpg",
                            "img/Andrena_flavipes_5795371_2.jpg",
                            "img/Andrena_flavipes_8430646_1.jpg"];
const pool_samples_fulva = ["img/Andrena_fulva_11872393_2.jpg",
                            "img/Andrena_fulva_15143858_1.jpg",
                            "img/Andrena_fulva_21366312_1.jpg",
                            "img/Andrena_fulva_21567123_1.jpg",
                            "img/Andrena_fulva_24609371_2.jpg",
                            "img/Andrena_fulva_24609371_6.jpg",
                            "img/Andrena_fulva_24752696_1.jpg",
                            "img/Andrena_fulva_25074448_1.jpg",
                            "img/Andrena_fulva_43114108_1.jpg",
                            "img/Andrena_fulva_43172780_1.jpg",
                            "img/Andrena_fulva_43270327_1.jpg",
                            "img/Andrena_fulva_43280860_1.jpg"];
const pool_samples_lucor = ["img/Bombus_terrestris_48029355_1.jpg",
                            "img/Bombus_terrestris_48056955_1.jpg",
                            "img/Bombus_terrestris_50405525_1.jpg",
                            "img/Bombus_terrestris_53709769_1.jpg",
                            "img/Bombus_terrestris_53737090_1.jpg",
                            "img/Bombus_terrestris_53835710_1.jpg",
                            "img/Bombus_terrestris_54871905_2.jpg",
                            "img/Bombus_terrestris_55046379_1.jpg",
                            "img/Bombus_terrestris_55141300_1.jpg",
                            "img/Bombus_terrestris_55204752_1.jpg",
                            "img/Bombus_terrestris_56168748_1.jpg",
                            "img/Bombus_terrestris_70317519_1.jpg"];

const pool_samples_13 = [pool_samples_flavi, pool_samples_fulva, pool_samples_lucor];

// Randomly pick samples out of pool for T1&3
const test_samples = [];
const labels_13 = Array(4).fill(classes[0]).concat(Array(4).fill(classes[1]), Array(4).fill(classes[2])); // needed for checking user's correctness

for (let i = 0; i < pool_samples_13.length; i++) {

  // Shuffle pool for current species
  for (let j = pool_samples_13[i].length - 1; j > 0; j--) {
    const k = Math.floor(Math.random() * (j + 1));
    [pool_samples_13[i][j], pool_samples_13[i][k]] = [pool_samples_13[i][k], pool_samples_13[i][j]];
  }

  // Add first new 6 samples to the list for T1&3
  for (let j = 0; j < 4; j++) {
    test_samples.push(pool_samples_13[i][j]);
  }
}

// Shuffle indexes for test samples in Tasks 1&3 (and their corresponding true labels)
// Otherwise, species order is not random
for (let i = test_samples.length - 1; i > 0; i--) {
  const j = Math.floor(Math.random() * (i + 1));
  [test_samples[i], test_samples[j]] = [test_samples[j], test_samples[i]];
  [labels_13[i], labels_13[j]] = [labels_13[j], labels_13[i]];
}

const test_samples_1 = test_samples.slice(0, 6);
const labels_1 = labels_13.slice(0, 6);
const test_samples_3 = test_samples.slice(6); // start at index 6 till the end
const labels_3 = labels_13.slice(6);

/*** Task 2 ***/
// Textual formulations of the given concepts
const natural_exps = ['it has a smooth shiny dark brown texture', 'it is fuzzy dark orange', 'it has fuzzy yellow and black stripes']
const natural_exps_neg = ['it does NOT have a smooth shiny dark brown texture',
                          'it is NOT fuzzy dark orange', 'it does NOT have fuzzy yellow and black stripes']

// Pool of correctly predicted samples (both cls and concept) - 5 will be picked
const pool_samples_correct = ["img/Andrena_flavipes_10588940_2.jpg",
                              "img/Andrena_flavipes_10588940_5.jpg",
                              "img/Andrena_flavipes_22101904_1.jpg",
                              "img/Andrena_flavipes_22465388_1.jpg",
                              "img/Andrena_flavipes_33484614_1.jpg",
                              "img/Andrena_fulva_12231414_2.jpg",
                              "img/Andrena_fulva_16795311_1.jpg",
                              "img/Andrena_fulva_24881697_3.jpg",
                              "img/Andrena_fulva_41623103_3.jpg",
                              "img/Andrena_fulva_41637839_1.jpg",
                              "img/Andrena_fulva_41705690_1.jpg",
                              "img/Bombus_terrestris_48213526_1.jpg",
                              "img/Bombus_terrestris_50304865_1.jpg",
                              "img/Bombus_terrestris_54307855_2.jpg",
                              "img/Bombus_terrestris_54718964_2.jpg"];
// Correct cls predictions
const labels_samples_correct = Array(5).fill(classes[0]).concat(Array(6).fill(classes[1]), Array(4).fill(classes[2]));
// Correct concept predictions
const exps_correct_flavi = natural_exps[0] + ' but ' + natural_exps_neg[1] + ' and ' + natural_exps_neg[2];
const exps_correct_fulva = natural_exps[1] + ' but ' + natural_exps_neg[0] + ' and ' + natural_exps_neg[2];
const exps_correct_lucor = natural_exps[2] + ' but ' + natural_exps_neg[0] + ' and ' + natural_exps_neg[1];
const exps_samples_correct = Array(5).fill(exps_correct_flavi).concat(Array(6).fill(exps_correct_fulva), Array(4).fill(exps_correct_lucor));

// Shuffle samples, true labels and true explanations (take first 5)
for (let i = pool_samples_correct.length - 1; i > 0; i--) {
  const j = Math.floor(Math.random() * (i + 1));
  [pool_samples_correct[i], pool_samples_correct[j]] = [pool_samples_correct[j], pool_samples_correct[i]];
  [labels_samples_correct[i], labels_samples_correct[j]] = [labels_samples_correct[j], labels_samples_correct[i]];
  [exps_samples_correct[i], exps_samples_correct[j]] = [exps_samples_correct[j], exps_samples_correct[i]];
}

const samples_correct = pool_samples_correct.slice(0, 5);
const labels_correct = labels_samples_correct.slice(0, 5); // would be same as preds_correct -> no need for extra array
const exps_correct = exps_samples_correct.slice(0, 5);

// Pool of wrongly predicted samples (neither cls, nor concept) - 1 will be picked
const pool_samples_wrong = ["img/Andrena_flavipes_68809988_1.jpg",
                            "img/Bombus_terrestris_67926127_1.jpg",
                            "img/Bombus_terrestris_93877801_3.jpg"];
// Wrong cls prediction and wrong explanations
// Note: every wrong sample was predicted A. fulva because fuzzy orange
const labels_wrong = ["Andrena flavipes", "Bombus lucorum", "Bombus lucorum"];
const pred_wrong = "Andrena fulva";
const exp_wrong = exps_correct_fulva;

// Pick one random wrongly predicted sample
wrong_ind = choose_group([0, 1, 2]);
const sample_wrong = pool_samples_wrong[wrong_ind];
const label_wrong = labels_wrong[wrong_ind];

// Concatenate and shuffle samples for Task 2, along with true labels, cls predictions and explanations
const test_samples_2 = samples_correct.concat(sample_wrong);
const labels_2 = labels_correct.concat(label_wrong);
const preds_2 = labels_correct.concat(pred_wrong);
const exps_2 = exps_correct.concat(exp_wrong);
for (let i = 0; i < test_samples_2.length; i++) {
  const j = Math.floor(Math.random() * (i + 1));
  [test_samples_2[i], test_samples_2[j]] = [test_samples_2[j], test_samples_2[i]];
  [labels_2[i], labels_2[j]] = [labels_2[j], labels_2[i]];
  [preds_2[i], preds_2[j]] = [preds_2[j], preds_2[i]];
  [exps_2[i], exps_2[j]] = [exps_2[j], exps_2[i]];
}

/*** UI ***/
// Grid with protos (just labels beneath, no buttons)
var proto_grid = `
      <div id="div_row">
          <div class="row">
              <div class="column">
                  <div class="card">
                      <img src="img/Andrena_flavipes_proto.jpg" alt="bico">
                      <h5>Andrena flavipes</h5>
                  </div>
              </div>

              <div class="column">
                  <div class="card">
                      <img src="img/Andrena_fulva_proto.jpg" alt="flavi">
                      <h5>Andrena fulva</h5>
                  </div>
              </div>

              <div class="column">
                  <div class="card">
                      <img src="img/Bombus_lucorum_proto.jpg" alt="fulva">
                      <h5>Bombus lucorum</h5>
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
             test_samples_2,
             test_samples_3]
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
if(assigned_group === 'A') {
    var text_task_2 = `Assign a species while also knowing our model's prediction (marked red in title).`;
} else if(assigned_group === 'B') {
    var text_task_2 = `Assign a species while also knowing our model's prediction and seeing an explanation for it (marked red in title).`;
}
var instructions = {
    type: jsPsychHtmlButtonResponse,
    stimulus: `	  
      <p>In this experiment, you will be shown 18 images of 3 
	wild bee species and be asked to solve three tasks.</p><p><strong>Task 1 (6 images)</strong>: Assign a species to the
	test image based on the prototypes shown on the right half of the page.</p>
      <p><strong>Task 2 (6 images)</strong>: ` + text_task_2 + `</p>
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
      `<div id="just_protos_prompt_div"><p>Before starting the experiment, take your time and look at the 3 samples on the right.
	Each of them was chosen as a prototype of their species. Throughout the whole experiment you will be shown these representative samples 
	next to the test samples to help you decide which species the test sample belongs to. 
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

var test_stimuli_2 = [];
for (let i = 0; i < test_samples_2.length; i++) {
  test_stimuli_2.push({stimulus: test_samples_2[i], correct_response: labels_2[i],
                       pred_class: preds_2[i], pred_concept: exps_2[i]});
};

var test_stimuli_3 = [];
for (let i = 0; i < test_samples_3.length; i++) {
  test_stimuli_3.push({stimulus: test_samples_3[i], correct_response: labels_3[i]});
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
        <p><strong>Task 2 (6 images): ` + text_task_2 + `</strong></p>`;
    },
    choices: ['Continue']
};
timeline.push(debrief_block_no_model_1);

/*** WITH PREDICTIONS ***/

if(assigned_group === 'A') {

    var test_with_pred = {
        type: jsPsychImageButtonResponse,
        stimulus: jsPsych.timelineVariable('stimulus'),
        choices: classes,
        data: {
          task: 'response_pred',
          correct_response: jsPsych.timelineVariable('correct_response'),
          pred_class: jsPsych.timelineVariable('pred_class')
        },
        on_finish: function(data){
          data.correct = jsPsych.pluginAPI.compareKeys(classes[data.response], data.correct_response);
        }
    };

} else if(assigned_group === 'B') {

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
}

var test_procedure_with_pred = {
    timeline: [fixation, test_with_pred],
    timeline_variables: test_stimuli_2,
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
    timeline_variables: test_stimuli_3,
    repetitions: 1,
    randomize_order: true
};
timeline.push(test_procedure_no_model_2);

if(assigned_group === 'A') {

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
            <p>Click <strong>Continue</strong> to end the experiment.</p>`;
        },
        choices: ['Continue']
    };
    timeline.push(debrief_block_no_model_2);

} else if(assigned_group == 'B') {

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
}

// Define goodbye message trial
var goodbye = {
    type: jsPsychHtmlButtonResponse,
    stimulus: "<strong>Thank you for participating! Have a nice day :^)</strong>",
    choices: ['Finish']
};
timeline.push(goodbye);

// Start the experiment
jsPsych.run(timeline);