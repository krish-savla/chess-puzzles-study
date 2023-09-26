/**
 * @title Chess Playing with Muse
 * @description Chess Playing with Muse
 * @version 0.1.0
 *
 * @assets assets/
 */

//ideas: 
// keep track of mouse movements. 
// 

// You can import stylesheets (.scss or .css).
import "../styles/main.scss";

import { initJsPsych } from "jspsych";

import fullscreen from '@jspsych/plugin-fullscreen';
import callFunction from '@jspsych/plugin-call-function';
import PreloadPlugin from "@jspsych/plugin-preload";
import htmlKeyboardResponse from '@jspsych/plugin-html-keyboard-response';
import jsPsychHtmlButtonResponse from '@jspsych/plugin-html-button-response';
import imageKeyboardResponse from '@jspsych/plugin-image-keyboard-response';

import { MuseClient, channelNames } from 'muse-js';
import { runPuzzle } from './runpuzzle.js';
import { ExpData } from './expdata.js';

import { inspect } from 'util';
import {v4} from 'uuid';
/**
 * This function will be executed by jsPsych Builder and is expected to run the jsPsych experiment
 *
 * @type {import("jspsych-builder").RunFunction}
 */
export async function run({ assetPaths, input = {}, environment, title, version }) {    
    
    var museClient;
    var DATA = new ExpData();

    const stims = ['assets/A.png', 'assets/B.png'];
    const numTrials = 100;

    const jsPsych = initJsPsych({
        on_finish: async function(data) {
            DATA.addTrialData(data);
            const save_data = DATA.toJSON();
            const blob = new Blob([ JSON.stringify(save_data) ]);
            const result = await fetch(`http://localhost:8080`, { method:"POST", body:blob });
            console.log(result);
        }
    });
    jsPsych.data.addProperties({subject_id: v4().slice(0,8)});

    const timeline = [];

    // Preload assets
    timeline.push({
        type: PreloadPlugin,
        images: assetPaths.images,
        audio: assetPaths.audio,
        video: assetPaths.video,
    });

    timeline.push({
        type: fullscreen,
        fullscreen_mode: true
    })
      
    var id =  document.createElement('button');
    id.id = "saveme";
    document.head.appendChild(id);
    
    document.getElementById("saveme").addEventListener("click", async function() {
        console.log("clicked")
        museClient = new MuseClient();
        museClient.enablePpg = true;
        await museClient.connect();
        await museClient.start();   
        DATA.addMuseClient(museClient);        
    });

    timeline.push({
        type: jsPsychHtmlButtonResponse, 
        button_html: "<button id='hello' onclick=saveme.click() class='jspsych-bntn' style='height:200px;width:200px'></button>",
        stimulus:  "<p>Press button below connect to the Muse Device.</p>",
        choices: ["yes"]
    });
  
    timeline.push({
        type: htmlKeyboardResponse,
        stimulus: "<p>When you see 'A', think 'A' - when you see 'B', think 'B'.</p>",
        choices: ['Enter']
    })

    var fixation = {
        type: htmlKeyboardResponse,
        stimulus: '<div style="font-size:60px;">+</div>',
        choices: "NO_KEYS",
        trial_duration: 150,
        on_start: () => {
            DATA.injectMuseMarker("fixation_loading");
        },
        on_load: () => {
            DATA.injectMuseMarker("fixation_started")
        },
        on_finish: (data) => {
            DATA.injectMuseMarker("fixation_ended");
        }
    };

    Array.prototype.random = function () {
        return this[Math.random() >= 0.5 ? 0 : 1];
    }
    function make_test() {
        let stimulus = stims.random()
        return {
            type: imageKeyboardResponse,
            stimulus: stimulus,
            choices: "NO_KEYS",
            stimulus_height: 400,
            stimulus_width: 400,
            trial_duration: 1000,
            post_trial_gap: 150,
            on_start: () => {
                DATA.injectMuseMarker(stimulus + "_trial_loading");
            },
            on_load: () => {
                DATA.injectMuseMarker(stimulus + "_trial_started")
            },
            on_finish: (data) => {
                DATA.injectMuseMarker(stimulus + "_trial_ended");
                DATA.addTrialData(data);
            }
        }
    };

    for (let i = 0; i < numTrials; i++) {
        timeline.push(fixation);
        timeline.push(make_test());
    }

    await jsPsych.run(timeline);

    // Return the jsPsych instance so jsPsych Builder can access the experiment results (remove this
    // if you handle results yourself, be it here or in `on_finish()`)
    return jsPsych;
}
