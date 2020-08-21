var urlMeta = {};

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message && message.payload && message.action === 'URL_PROCESSED') {
    var className=message.payload.predictions['className'];
    console.log(className)
    confirm(`Url=${message.payload.url}`+'\n\nThis seems like a '+`${className}`+' url')
  }
});