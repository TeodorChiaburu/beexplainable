var jsPsychImageButtonResponse = (function (jspsych) {
  'use strict';

  const info = {
      name: "image-button-response",
      parameters: {
          /** The image to be displayed */
          stimulus: {
              type: jspsych.ParameterType.IMAGE,
              pretty_name: "Stimulus",
              default: undefined,
          },
          /** Set the image height in pixels */
          stimulus_height: {
              type: jspsych.ParameterType.INT,
              pretty_name: "Image height",
              default: null,
          },
          /** Set the image width in pixels */
          stimulus_width: {
              type: jspsych.ParameterType.INT,
              pretty_name: "Image width",
              default: null,
          },
          /** Maintain the aspect ratio after setting width or height */
          maintain_aspect_ratio: {
              type: jspsych.ParameterType.BOOL,
              pretty_name: "Maintain aspect ratio",
              default: true,
          },
          /** Array containing the label(s) for the button(s). */
          choices: {
              type: jspsych.ParameterType.STRING,
              pretty_name: "Choices",
              default: undefined,
              array: true,
          },
          /** The HTML for creating button. Can create own style. Use the "%choice%" string to indicate where the label from the choices parameter should be inserted. */
          button_html: {
              type: jspsych.ParameterType.HTML_STRING,
              pretty_name: "Button HTML",
              default: '<button class="jspsych-btn">%choice%</button>',
              array: true,
          },
          /** Any content here will be displayed under the button. */
          prompt: {
              type: jspsych.ParameterType.HTML_STRING,
              pretty_name: "Prompt",
              default: null,
          },
          /** How long to show the stimulus. */
          stimulus_duration: {
              type: jspsych.ParameterType.INT,
              pretty_name: "Stimulus duration",
              default: null,
          },
          /** How long to show the trial. */
          trial_duration: {
              type: jspsych.ParameterType.INT,
              pretty_name: "Trial duration",
              default: null,
          },
          /** The vertical margin of the button. */
          margin_vertical: {
              type: jspsych.ParameterType.STRING,
              pretty_name: "Margin vertical",
              default: "0px",
          },
          /** The horizontal margin of the button. */
          margin_horizontal: {
              type: jspsych.ParameterType.STRING,
              pretty_name: "Margin horizontal",
              default: "8px",
          },
          /** If true, then trial will end when user responds. */
          response_ends_trial: {
              type: jspsych.ParameterType.BOOL,
              pretty_name: "Response ends trial",
              default: true,
          },
          /**
           * If true, the image will be drawn onto a canvas element (prevents blank screen between consecutive images in some browsers).
           * If false, the image will be shown via an img element.
           */
          render_on_canvas: {
              type: jspsych.ParameterType.BOOL,
              pretty_name: "Render on canvas",
              default: true,
          },
      },
  };

  /**
   * **image-button-response**
   *
   * jsPsych plugin for displaying an image stimulus and getting a button response
   *
   * @author Josh de Leeuw
   * @see {@link https://www.jspsych.org/plugins/jspsych-image-button-response/ image-button-response plugin documentation on jspsych.org}
   */
  class ImageButtonResponsePlugin {
      constructor(jsPsych) {
          this.jsPsych = jsPsych;
      }

      trial(display_element, trial) {
          var height, width;
          var html;
          if (trial.render_on_canvas) {
              var image_drawn = false;
              // first clear the display element (because the render_on_canvas method appends to display_element instead of overwriting it with .innerHTML)
              if (display_element.hasChildNodes()) {
                  // can't loop through child list because the list will be modified by .removeChild()
                  while (display_element.firstChild) {
                      display_element.removeChild(display_element.firstChild);
                  }
              }
              // create title div with the prompt question
              var div_title = document.createElement("div");
              div_title.className = "container";
              div_title.id = "div_title";
              div_title.innerHTML += "<h4>What species do you think the insect on the left is? Hover to zoom in.</h4>";
              if (typeof trial.data.pred_class !== 'undefined' && typeof trial.data.pred_concept === 'undefined') {
                  div_title.innerHTML += "<h5>Our model predicted " + trial.data.pred_class + ".</h5>";
              }
              else if (typeof trial.data.pred_class !== 'undefined' && typeof trial.data.pred_concept !== 'undefined') {
                  div_title.innerHTML += "<h5>Our model predicted " + trial.data.pred_class + " because:</h5>";
                  div_title.innerHTML += "<h5>" + trial.data.pred_concept + "</h5>";
              }
              //div_title.innerHTML += "<h5>(hover over the image to zoom in)</h5>";
              display_element.insertBefore(div_title, null);

              // create div for canvas-image and zoom-pane
              var div_canvas_zoom = document.createElement("div");
              div_canvas_zoom.className = "img-zoom-container column";
              div_canvas_zoom.style.margin = "0 50px 0 50px";
              div_canvas_zoom.style.padding = "0";
              div_canvas_zoom.style.width = "20%";

              // create canvas element and image
              var canvas = document.createElement("canvas");
              canvas.id = "jspsych-image-button-response-stimulus";
              canvas.classList.add("card");
              canvas.style.aspectRatio = "1 / 1";

              var ctx = canvas.getContext("2d");
              var img = new Image();
              img.onload = () => {
                  // if image wasn't preloaded, then it will need to be drawn whenever it finishes loading
                  if (!image_drawn) {
                      getHeightWidth(); // only possible to get width/height after image loads
                      ctx.drawImage(img, 0, 0, width, height);
                  }
              };
              img.src = trial.stimulus;
              // get/set image height and width - this can only be done after image loads because uses image's naturalWidth/naturalHeight properties
              const getHeightWidth = () => {
                  if (trial.stimulus_height !== null) {
                      height = trial.stimulus_height;
                      if (trial.stimulus_width == null && trial.maintain_aspect_ratio) {
                          width = img.naturalWidth * (trial.stimulus_height / img.naturalHeight);
                      }
                  }
                  else {
                      height = img.naturalHeight;
                  }
                  if (trial.stimulus_width !== null) {
                      width = trial.stimulus_width;
                      if (trial.stimulus_height == null && trial.maintain_aspect_ratio) {
                          height = img.naturalHeight * (trial.stimulus_width / img.naturalWidth);
                      }
                  }
                  else if (!(trial.stimulus_height !== null && trial.maintain_aspect_ratio)) {
                      // if stimulus width is null, only use the image's natural width if the width value wasn't set
                      // in the if statement above, based on a specified height and maintain_aspect_ratio = true
                      width = img.naturalWidth;
                  }
                  canvas.height = height;
                  canvas.width = width;
              };
              getHeightWidth(); // call now, in case image loads immediately (is cached)

              // create buttons
              var buttons = [];
              if (Array.isArray(trial.button_html)) {
                  if (trial.button_html.length == trial.choices.length) {
                      buttons = trial.button_html;
                  }
                  else {
                      console.error("Error in image-button-response plugin. The length of the button_html array does not equal the length of the choices array");
                  }
              }
              else {
                  for (var i = 0; i < trial.choices.length; i++) {
                      buttons.push(trial.button_html);
                  }
              }
              var btngroup_div = document.createElement("div");
              btngroup_div.id = "div_row";
              html = '';

              // Note: when having 5 prototypes, the grid needs a 6th dummy cell to ensure clean display
              for (var i = 0; i < trial.choices.length+1; i++) {
                  // only add an extra div of class "row" every three images
                  if(i%3 == 0) {
                      html += '<div class="row">';
                  };

                  if(i == trial.choices.length) {
                      html +=
                          '<div class="column"></div>'; // dummy cell with no image
                  } else {
                      var str = buttons[i].replace(/%choice%/g, trial.choices[i]); // the button tag along with the class label
                      var img_path = "img/" + trial.choices[i].replace(" ", "_") + "_proto.jpg";

                      html +=
                          '<div class="column">' +
                          '<div class="card">' +
                          '<img src="' + img_path + '">' +
                          '<div class="container jspsych-image-button-response-button" id="jspsych-image-button-response-button-' + i + '" data-choice="' + i + '">' +
                          '<p><button class="button"><strong>' + trial.choices[i] + '</strong></button></p>' +
                          //str +
                          '</div>' +
                          '</div>' +
                          '</div>';
                  }

                  // close 'row' div after every 3 images
                  if(i%3 == 2) {
                      html += '</div>';
                  };
              }
              //html += '</div>'; // div_row
              btngroup_div.innerHTML = html;

              if (img.complete && Number.isFinite(width) && Number.isFinite(height)) {
                  // if image has loaded and width/height have been set, then draw it now
                  // (don't rely on img onload function to draw image when image is in the cache, because that causes a delay in the image presentation)
                  ctx.drawImage(img, 0, 0, width, height);
                  image_drawn = true;
              }

              // create pane for zoom-in
              var zoom_div = document.createElement("div");
              zoom_div.className = "img-zoom-result";
              zoom_div.id = "zoom_result";
              zoom_div.classList.add("card");
              zoom_div.style.margin = "auto";

              // add canvas-image and zoom-pane to the same div with position=relative (necessary for the zoom function)
              div_canvas_zoom.appendChild(canvas);
              div_canvas_zoom.appendChild(zoom_div);
              display_element.insertBefore(div_canvas_zoom, null);

              // Zoom in on images
              function imageZoom(imgID, resultID) {
                var img, lens, result, zoom_scale;
                const IMG_SCREEN = 0.17093; // hack for getting true width of the displayed image: img_width / window_width is const.
                var img_width = window.innerWidth * IMG_SCREEN;
                // Note: since image pane and resulting zooming pane are quadratic
                //       then img_width = img_height = result_width = result_height
                //       Also the lens is quadratic, so lens_width = lens_height

                img = document.getElementById(imgID);
                result = document.getElementById(resultID);

                /*create lens in sized down displayed image*/
                lens = document.createElement("div");
                lens.setAttribute("class", "img-zoom-lens");
                img.parentElement.insertBefore(lens, img);

                /*calculate the ratio between result div and lens:*/
                zoom_scale = img_width / lens.offsetWidth;

                /*set background properties for the result div:*/
                result.style.backgroundImage = "url('" + trial.stimulus + "')";
                result.style.backgroundSize = (img_width * zoom_scale) + "px " + (img_width * zoom_scale) + "px";

                //TODO
                /*set zoomed patch in the center of the image before moving the lense*/
                //result.style.backgroundPosition = "-" + ((lens.offsetLeft - img.offsetLeft + lens.offsetWidth/2) * zoom_scale) + "px -" +
                //    ((lens.offsetTop + lens.offsetWidth/2) * zoom_scale) + "px";

                /*execute a function when someone moves the cursor over the image, or the lens:*/
                lens.addEventListener("mousemove", moveLens);
                img.addEventListener("mousemove", moveLens);
                /*and also for touch screens:*/
                lens.addEventListener("touchmove", moveLens);
                img.addEventListener("touchmove", moveLens);

                function moveLens(e) {
                    var pos, x, y;
                    /*prevent any other actions that may occur when moving over the image:*/
                    e.preventDefault();
                    /*get the cursor's x and y positions:*/
                    pos = getCursorPos(e);
                    /*calculate the position of the lens in displayed image*/
                    x = pos.x - (lens.offsetWidth / 2) + img.offsetLeft;
                    y = pos.y - (lens.offsetHeight / 2);
                    /*prevent the lens from being positioned outside the image:*/
                    if (x > img_width + img.offsetLeft - lens.offsetWidth) {
                        x = img_width + img.offsetLeft - lens.offsetWidth;
                    }
                    if (x < img.offsetLeft) {
                        x = img.offsetLeft;
                    }
                    if (y > img_width - lens.offsetHeight) {
                        y = img_width - lens.offsetHeight;
                    }
                    if (y < 0) {
                        y = 0;
                    }
                    /*set the position of the lens:*/
                    lens.style.left = x + "px";
                    lens.style.top = y + "px";
                    /*display what the lens "sees":*/
                    result.style.backgroundPosition = "-" + ((x - img.offsetLeft) * zoom_scale) + "px -" + (y * zoom_scale) + "px";
                }

                function getCursorPos(e) {
                    var a, x = 0, y = 0;
                    e = e || window.Event;
                    /*get the x and y positions of the image:*/
                    a = img.getBoundingClientRect();
                    /*calculate the cursor's x and y coordinates, relative to the image:*/
                    x = e.pageX - a.left;
                    y = e.pageY - a.top;
                    /*consider any page scrolling:*/
                    x = x - window.scrollX;
                    y = y - window.scrollY;
                    return {x : x, y : y};
                }
              };
              // Initiate zoom effect
              imageZoom("jspsych-image-button-response-stimulus", "zoom_result");

              // add buttons to screen
              display_element.insertBefore(btngroup_div, div_canvas_zoom.nextElementSibling);
              // add prompt if there is one
              if (trial.prompt !== null) {
                  display_element.insertAdjacentHTML("beforeend", trial.prompt);
              }
          }
          else {
              // display stimulus as an image element
              html = '<img src="' + trial.stimulus + '" id="jspsych-image-button-response-stimulus">';
              //display buttons
              var buttons = [];
              if (Array.isArray(trial.button_html)) {
                  if (trial.button_html.length == trial.choices.length) {
                      buttons = trial.button_html;
                  }
                  else {
                      console.error("Error in image-button-response plugin. The length of the button_html array does not equal the length of the choices array");
                  }
              }
              else {
                  for (var i = 0; i < trial.choices.length; i++) {
                      buttons.push(trial.button_html);
                  }
              }
              html += '<div id="jspsych-image-button-response-btngroup">';
              for (var i = 0; i < trial.choices.length; i++) {
                  var str = buttons[i].replace(/%choice%/g, trial.choices[i]);
                  html +=
                      '<div class="jspsych-image-button-response-button" style="display: inline-block; margin:' +
                          trial.margin_vertical +
                          " " +
                          trial.margin_horizontal +
                          '" id="jspsych-image-button-response-button-' +
                          i +
                          '" data-choice="' +
                          i +
                          '">' +
                          str +
                          "</div>";
              }
              html += "</div>";
              // add prompt
              if (trial.prompt !== null) {
                  html += trial.prompt;
              }
              // update the page content
              display_element.innerHTML = html;
              // set image dimensions after image has loaded (so that we have access to naturalHeight/naturalWidth)
              var img = display_element.querySelector("#jspsych-image-button-response-stimulus");
              if (trial.stimulus_height !== null) {
                  height = trial.stimulus_height;
                  if (trial.stimulus_width == null && trial.maintain_aspect_ratio) {
                      width = img.naturalWidth * (trial.stimulus_height / img.naturalHeight);
                  }
              }
              else {
                  height = img.naturalHeight;
              }
              if (trial.stimulus_width !== null) {
                  width = trial.stimulus_width;
                  if (trial.stimulus_height == null && trial.maintain_aspect_ratio) {
                      height = img.naturalHeight * (trial.stimulus_width / img.naturalWidth);
                  }
              }
              else if (!(trial.stimulus_height !== null && trial.maintain_aspect_ratio)) {
                  // if stimulus width is null, only use the image's natural width if the width value wasn't set
                  // in the if statement above, based on a specified height and maintain_aspect_ratio = true
                  width = img.naturalWidth;
              }
              img.style.height = height.toString() + "px";
              img.style.width = width.toString() + "px";
          }
          // start timing
          var start_time = performance.now();
          for (var i = 0; i < trial.choices.length; i++) {
              display_element
                  .querySelector("#jspsych-image-button-response-button-" + i)
                  .addEventListener("click", (e) => {
                  var btn_el = e.currentTarget;
                  var choice = btn_el.getAttribute("data-choice"); // don't use dataset for jsdom compatibility
                  after_response(choice);
              });
          }
          // store response
          var response = {
              rt: null,
              button: null,
          };
          // function to end trial when it is time
          const end_trial = () => {
              // kill any remaining setTimeout handlers
              this.jsPsych.pluginAPI.clearAllTimeouts();
              // gather the data to store for the trial
              var trial_data = {
                  rt: response.rt,
                  stimulus: trial.stimulus,
                  response: response.button,
              };
              // clear the display
              display_element.innerHTML = "";
              // move on to the next trial
              this.jsPsych.finishTrial(trial_data);
          };
          // function to handle responses by the subject
          function after_response(choice) {
              // measure rt
              var end_time = performance.now();
              var rt = Math.round(end_time - start_time);
              response.button = parseInt(choice);
              response.rt = rt;
              // after a valid response, the stimulus will have the CSS class 'responded'
              // which can be used to provide visual feedback that a response was recorded
              display_element.querySelector("#jspsych-image-button-response-stimulus").className +=
                  " responded";
              // disable all the buttons after a response
              var btns = document.querySelectorAll(".jspsych-image-button-response-button button");
              for (var i = 0; i < btns.length; i++) {
                  //btns[i].removeEventListener('click');
                  btns[i].setAttribute("disabled", "disabled");
              }
              if (trial.response_ends_trial) {
                  end_trial();
              }
          }
          // hide image if timing is set
          if (trial.stimulus_duration !== null) {
              this.jsPsych.pluginAPI.setTimeout(() => {
                  display_element.querySelector("#jspsych-image-button-response-stimulus").style.visibility = "hidden";
              }, trial.stimulus_duration);
          }
          // end trial if time limit is set
          if (trial.trial_duration !== null) {
              this.jsPsych.pluginAPI.setTimeout(() => {
                  end_trial();
              }, trial.trial_duration);
          }
          else if (trial.response_ends_trial === false) {
              console.warn("The experiment may be deadlocked. Try setting a trial duration or set response_ends_trial to true.");
          }
      }
      simulate(trial, simulation_mode, simulation_options, load_callback) {
          if (simulation_mode == "data-only") {
              load_callback();
              this.simulate_data_only(trial, simulation_options);
          }
          if (simulation_mode == "visual") {
              this.simulate_visual(trial, simulation_options, load_callback);
          }
      }
      create_simulation_data(trial, simulation_options) {
          const default_data = {
              stimulus: trial.stimulus,
              rt: this.jsPsych.randomization.sampleExGaussian(500, 50, 1 / 150, true),
              response: this.jsPsych.randomization.randomInt(0, trial.choices.length - 1),
          };
          const data = this.jsPsych.pluginAPI.mergeSimulationData(default_data, simulation_options);
          this.jsPsych.pluginAPI.ensureSimulationDataConsistency(trial, data);
          return data;
      }
      simulate_data_only(trial, simulation_options) {
          const data = this.create_simulation_data(trial, simulation_options);
          this.jsPsych.finishTrial(data);
      }
      simulate_visual(trial, simulation_options, load_callback) {
          const data = this.create_simulation_data(trial, simulation_options);
          const display_element = this.jsPsych.getDisplayElement();
          this.trial(display_element, trial);
          load_callback();
          if (data.rt !== null) {
              this.jsPsych.pluginAPI.clickTarget(display_element.querySelector(`div[data-choice="${data.response}"] button`), data.rt);
          }
      }
  }
  ImageButtonResponsePlugin.info = info;

  return ImageButtonResponsePlugin;

})(jsPsychModule);
