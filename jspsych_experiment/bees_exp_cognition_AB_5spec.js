/*** UI for HIL-Experiment ***/


// Initialize jsPsych
var jsPsych = initJsPsych({
  show_progress_bar: false
});

// Randomly pick whether user will be assigned to group A (Control) or B (XAI)
groups = ['A', 'B'];
function choose_group(groups) {
  var index = Math.floor(Math.random() * groups.length);
  return groups[index];
}
assigned_group = choose_group(groups);

// Create timeline
var timeline = [];
const protos = ["img/Andrena_bicolor_proto.jpg", "img/Andrena_flavipes_proto.jpg", "img/Andrena_fulva_proto.jpg",
                "img/Bombus_lucorum_proto.jpg", "img/Bombus_pratorum_proto.jpg"];

// The 3 possible classes
const classes = ["Andrena bicolor", "Andrena flavipes", "Andrena fulva", "Bombus lucorum", "Bombus pratorum"];

/*** Tasks 1 and 3 ***/
// Sample pools for Tasks 1 and 3 (only 4 will be randomly picked for each species)
const pool_samples_bicol = ["img/Andrena_bicolor_39411385_1.jpg",
                            "img/Andrena_bicolor_39748872_3.jpg",
                            "img/Andrena_bicolor_40186737_3.jpg",
                            "img/Andrena_bicolor_42078638_3.jpg",
                            "img/Andrena_bicolor_44969462_2.jpg",
                            "img/Andrena_bicolor_70513296_3.jpg",
                            "img/Andrena_bicolor_70615494_2.jpg",
                            "img/Andrena_bicolor_70744142_2.jpg",
                            "img/Andrena_bicolor_70836009_2.jpg",
                            "img/Andrena_bicolor_71944410_2.jpg",
                            "img/Andrena_bicolor_72391501_2.jpg",
                            "img/Andrena_bicolor_97033019_1.jpg"];
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
const pool_samples_prato = ["img/Bombus_pratorum_20908187_1.jpg",
                            "img/Bombus_pratorum_21992207_1.jpg",
                            "img/Bombus_pratorum_22806096_1.jpg",
                            "img/Bombus_pratorum_26670234_1.jpg",
                            "img/Bombus_pratorum_26880403_1.jpg",
                            "img/Bombus_pratorum_26908927_1.jpg",
                            "img/Bombus_pratorum_27515055_2.jpg",
                            "img/Bombus_pratorum_45583159_2.jpg",
                            "img/Bombus_pratorum_45761945_1.jpg",
                            "img/Bombus_pratorum_47251573_1.jpg",
                            "img/Bombus_pratorum_47520957_1.jpg",
                            "img/Bombus_pratorum_48445878_2.jpg"];

const pool_samples_13 = [pool_samples_bicol, pool_samples_flavi, pool_samples_fulva,
                         pool_samples_lucor, pool_samples_prato];

// Randomly pick samples out of pool for T1&3
const num_drawn = 4
const test_samples = [];
const labels_13 = Array(num_drawn).fill(classes[0]).concat(Array(num_drawn).fill(classes[1]), Array(num_drawn).fill(classes[2]),
                                                           Array(num_drawn).fill(classes[3]), Array(num_drawn).fill(classes[4])); // needed for checking user's correctness

for (let i = 0; i < pool_samples_13.length; i++) {

  // Shuffle pool for current species
  for (let j = pool_samples_13[i].length - 1; j > 0; j--) {
    const k = Math.floor(Math.random() * (j + 1));
    [pool_samples_13[i][j], pool_samples_13[i][k]] = [pool_samples_13[i][k], pool_samples_13[i][j]];
  }

  // Add first new 4 samples to the list for T1&3
  for (let j = 0; j < num_drawn; j++) {
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

const num_samples_per_task = num_drawn * classes.length / 2;
const test_samples_1 = test_samples.slice(0, num_samples_per_task);
const labels_1 = labels_13.slice(0, num_samples_per_task);
const test_samples_3 = test_samples.slice(num_samples_per_task); // start at index i till the end
const labels_3 = labels_13.slice(num_samples_per_task);

/*** Task 2 ***/
// Pool of correctly predicted samples (both cls and concept)
const pool_samples_correct =   ["img/Andrena_bicolor_2799379_1.jpg",
                                "img/Andrena_bicolor_70836009_4.jpg",
                                "img/Andrena_flavipes_70667186_1.jpg",
                                "img/Andrena_flavipes_71664833_1.jpg",
                                "img/Andrena_flavipes_73411496_1.jpg",
                                "img/Andrena_flavipes_74766389_2.jpg",
                                "img/Andrena_flavipes_77801499_2.jpg",
                                "img/Andrena_fulva_77615356_2.jpg",
                                "img/Andrena_fulva_77876860_3.jpg",
                                "img/Andrena_fulva_78200707_1.jpg",
                                "img/Andrena_fulva_78437226_1.jpg",
                                "img/Andrena_fulva_78969818_1.jpg",
                                "img/Bombus_terrestris_72551957_1.jpg",
                                "img/Bombus_terrestris_72678063_1.jpg",
                                "img/Bombus_terrestris_72770462_2.jpg",
                                "img/Bombus_terrestris_72867045_1.jpg",
                                "img/Bombus_terrestris_73531362_1.jpg",
                                "img/Bombus_pratorum_21985654_1.jpg",
                                "img/Bombus_pratorum_42078196_1.jpg",
                                "img/Bombus_pratorum_45797034_2.jpg",
                                "img/Bombus_pratorum_45862602_1.jpg",
                                "img/Bombus_pratorum_58000679_1.jpg"];

// Correct cls predictions
const labels_samples_correct = Array(2).fill(classes[0]).concat(Array(5).fill(classes[1]), Array(5).fill(classes[2]),
                                                                          Array(5).fill(classes[3]), Array(5).fill(classes[4]));

// Correct concept predictions (for series brown - orange - yellow)
const exps_correct_bicol = 'shiny_brown fuzzy_orange not_fuzzy_yellow'; //'YES YES NO';
const exps_correct_flavi = 'shiny_brown not_fuzzy_orange not_fuzzy_yellow'; //'YES NO NO';
const exps_correct_fulva = 'not_shiny_brown fuzzy_orange not_fuzzy_yellow'; //'NO YES NO';
const exps_correct_lucor = 'not_shiny_brown not_fuzzy_orange fuzzy_yellow'; //'NO NO YES';
const exps_correct_prato = 'not_shiny_brown fuzzy_orange fuzzy_yellow'; //'NO YES YES';

const exps_samples_correct = Array(2).fill(exps_correct_bicol).concat(Array(5).fill(exps_correct_flavi), Array(5).fill(exps_correct_fulva),
                                                                                Array(5).fill(exps_correct_lucor), Array(5).fill(exps_correct_prato));

// Shuffle samples, true labels and true explanations
for (let i = pool_samples_correct.length - 1; i > 0; i--) {
  const j = Math.floor(Math.random() * (i + 1));
  [pool_samples_correct[i], pool_samples_correct[j]] = [pool_samples_correct[j], pool_samples_correct[i]];
  [labels_samples_correct[i], labels_samples_correct[j]] = [labels_samples_correct[j], labels_samples_correct[i]];
  [exps_samples_correct[i], exps_samples_correct[j]] = [exps_samples_correct[j], exps_samples_correct[i]];
}
const num_wrong_samples   = 2;
const num_correct_samples = num_samples_per_task - num_wrong_samples;
const samples_correct     = pool_samples_correct.slice(0, num_correct_samples);
const labels_correct      = labels_samples_correct.slice(0, num_correct_samples); // would be same as preds_correct -> no need for extra array
const exps_correct        = exps_samples_correct.slice(0, num_correct_samples);

// Pool of wrongly predicted samples (neither cls, nor concept)
const pool_samples_wrong = ["img/Andrena_bicolor_44969462_15.jpg",
                            "img/Andrena_fulva_76966123_1.jpg",
                            "img/Bombus_terrestris_74551267_1.jpg",
                            "img/Bombus_pratorum_41522167_1.jpg"];
// Wrong cls prediction and wrong explanations
// Note: the wrong explanations match the wrong predicted classes i.e. A.flavipes because brown
const labels_samples_wrong = ["Andrena bicolor", "Andrena fulva", "Bombus lucorum", "Bombus pratorum"];
const preds_samples_wrong  = ["Andrena flavipes", "Andrena bicolor", "Bombus pratorum", "Bombus lucorum"];
const exps_samples_wrong   = [exps_correct_flavi, exps_correct_bicol, exps_correct_prato, exps_correct_lucor];

// Shuffle samples, true labels, wrong predictions and wrong explanations
for (let i = pool_samples_wrong.length - 1; i > 0; i--) {
  const j = Math.floor(Math.random() * (i + 1));
  [pool_samples_wrong[i], pool_samples_wrong[j]] = [pool_samples_wrong[j], pool_samples_wrong[i]];
  [labels_samples_wrong[i], labels_samples_wrong[j]] = [labels_samples_wrong[j], labels_samples_wrong[i]];
  [preds_samples_wrong[i], preds_samples_wrong[j]] = [preds_samples_wrong[j], preds_samples_wrong[i]];
  [exps_samples_wrong[i], exps_samples_wrong[j]] = [exps_samples_wrong[j], exps_samples_wrong[i]];
}

// Pick the first new num_wrong_samples
const samples_wrong = pool_samples_wrong.slice(0, num_wrong_samples);
const labels_wrong  = labels_samples_wrong.slice(0, num_wrong_samples);
const preds_wrong   = preds_samples_wrong.slice(0, num_wrong_samples);
const exps_wrong    = exps_samples_wrong.slice(0, num_wrong_samples);

// Concatenate and shuffle samples for Task 2, along with true labels, cls predictions and explanations
const test_samples_2 = samples_correct.concat(samples_wrong);
const labels_2       = labels_correct.concat(labels_wrong);
const preds_2        = labels_correct.concat(preds_wrong);
const exps_2         = exps_correct.concat(exps_wrong);
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
          
          <div class="column">
              
          </div>
      </div>
  </div>`;

// Preload images
var preload = {
    type: jsPsychPreload,
    images: [protos,
             test_samples_1,
             test_samples_2,
             test_samples_3]
};
timeline.push(preload);

// Define welcome message
var welcome = {
    type: jsPsychHtmlButtonResponse,
    stimulus: `<strong>Welcome to the <i>beexplainable</i> experiment!</strong>
               <p><i>Note</i>: Please only do this experiment <strong>once</strong>.</p>
               <p>We also recommend you use a device with a wider screen (i.e. laptop, tablet) <strong>not</strong> your phone.`,
    choices: ['Continue']
};
timeline.push(welcome);

// Define instructions trial
if(assigned_group === 'A') {
    var text_task_2 = `Assign a species while also knowing our model's prediction (marked red in title).`;
    var text_quest  = ``;
} else if(assigned_group === 'B') {
    var text_task_2 = `Assign a species while also knowing our model's prediction and seeing an explanation for it (marked red in title).`;
    var text_quest  = `<p>After these tasks, you will be asked to rate 4 statements regarding your experience 
	throughout the experiment.</p>`;
}
const num_samples_total = num_samples_per_task * 3;
var instructions = {
    type: jsPsychHtmlButtonResponse,
    stimulus: `	  
      <p>In this experiment, you will be shown ${num_samples_total} images of ${classes.length} 
	wild bee species and be asked to solve three tasks.</p><p><strong>Task 1 (${num_samples_per_task} images)</strong>: Assign a species to the
	test image based on the prototypes shown on the right half of the page.</p>
      <p><strong>Task 2 (${num_samples_per_task} images)</strong>: ` + text_task_2 + `</p>
	    <p><strong>Task 3 (${num_samples_per_task} images)</strong>: Assign again a species only with the help of the prototypes 
	    (no model prediction revealed).</p>`
	    + text_quest +
	    `<p><i>Note</i>: From this moment on, please avoid resizing your browser window, as this may cause 
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
      `<div id="just_protos_prompt_div"><p>Before starting the experiment, take your time and look at the ${classes.length} samples on the right.
	Each of them was chosen as a prototype of their species. Throughout the whole experiment you will be shown these representative samples 
	next to the test samples to help you decide which species the test sample belongs to. 
	<p>Whenever you are ready, click <strong>Continue</strong> to start the first task:</p>
	<p><strong>Task 1 (${num_samples_per_task} images): Assign a species to the
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
        <p><strong>Task 2 (${num_samples_per_task} images): ` + text_task_2 + `</strong></p>`;
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
        <p><strong>Task 3 (${num_samples_per_task} images): Assign again a species only with the help of the prototypes 
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