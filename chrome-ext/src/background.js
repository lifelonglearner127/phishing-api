import 'babel-polyfill';
import axios from 'axios';

import { PHISHING_CLASSES } from './phishing_classes';


//change this base url to point to the server production url
const BASE_URL = 'http://0.0.0.0:5005'

class BackgroundProcessing {
  constructor() {
    this.imageRequests = {};
    this.addListeners();
    this.testApiReadiness();
  }

  
 // listen to user web interactions  every time a user visits a browser get the url to submit to the model backend
  addListeners() {
    chrome.tabs.onUpdated.addListener((tabId, changeInfo, tabInfo) => {
        if (changeInfo.status == "loading") {
            let currentURL = tabInfo.url;
            if(currentURL && currentURL.indexOf("devtools") == -1 && currentURL.indexOf("chrome://") == -1) {
                this.imageRequests[currentURL] = tabInfo;
                this.analyzeUrl(currentURL);
            }
        }
    });
  }

  // test backend api readiness 
  async testApiReadiness() {
    const startTime = performance.now();
    console.log('Checking model api readiness...');
    axios.get(BASE_URL+'/api_readiness')
      .then((response)=> {
        console.log(response.data)
        this.api = true;
        const totalTime = Math.floor(performance.now() - startTime);
        console.log(`Api ready, response time ${totalTime}ms...`);
      },(error) => {
        console.log(error);
        console.log("Api not ready ....")
      });
  }

  getTopClass(logits) {
    function indexOfMax(arr) {
      if (arr.length === 0) {
        return -1;
      }

      var max = arr[0];
      var maxIndex = 0;

      for (var i = 1; i < arr.length; i++) {
        if (arr[i] > max) {
          maxIndex = i;
          max = arr[i];
        }
      }

      return maxIndex;
    }
    var maxIndex = indexOfMax(logits);

    var topClass = {
      className: PHISHING_CLASSES[maxIndex]
    };
    return topClass;
  }

//predict function that calls the model endpoint
//   async predict(url) {
//     console.log('Predicting...');
//     const startTime = performance.now();
//     axios.post(BASE_URL+'/url',{
//       url: url
//     })
//       .then((response)=>{
//         console.log(response.data);
//         const totalTime = Math.floor(performance.now() - startTime);
//         console.log(`Prediction done in ${totalTime}ms`);
//         let res = response.data;
//         console.log(res)
//         let prediction = JSON.parse(res['prediction']);
//         const top_class = this.getTopClass(prediction);
//         console.log(top_class);
//         return top_class;
//       },(error) => {
//         console.log(error);
//       });
//   }

// url analyses entry point
  async analyzeUrl(url) {
    if (!this.api) {
      console.log('Api not loaded yet, delaying with 5 sec...');
      setTimeout(() => { this.analyzeUrl(url) }, 5000);
      return;
    }
    var meta = this.imageRequests[url];
    console.log(`Predicting ${url}...`);
    const startTime = performance.now();
    axios.post(BASE_URL+'/url',{
      url: url
    })
    .then((response)=>{
      console.log(response.data);
      const totalTime = Math.floor(performance.now() - startTime);
      console.log(`Prediction done in ${totalTime}ms`);
      let res = response.data;
      let prediction = JSON.parse(res['prediction']);
      const top_class = this.getTopClass(prediction);
      if (top_class['className'] == 'phishing') {
        meta.predictions = top_class
        chrome.tabs.sendMessage(meta.id, {
          action: 'URL_PROCESSED',
          payload: meta,
        })
      }
    },(error) => {
      console.log(error);

    });
  }
}

var bg = new BackgroundProcessing();

