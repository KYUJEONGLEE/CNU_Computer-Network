var skip_index = 0;
var remove_index = 0;
async function fetchRequestWithError() {
  try {
    skip_index = skip_index;
    const url = 'http://localhost:8080/pastebin/api/pastes/?skip='+skip_index;
    const response = await fetch(url);
    var key_arr = new Array();
    if (response.status >= 200 && response.status < 400) {
        const data = await response.json();
        for (var key in data){
            ndiv = document.createElement('div');
            ndiv.innerHTML = `<h2> ${data[key]['title']}</h2><p> ${data[key]['content']}</p><hr>`;
            pdiv = document.getElementById('newsfeed');
            pdiv.appendChild(ndiv);
            skip_index += 1;
            remove_index += 1;
            while(remove_index > 10){
                pdiv.removeChild(pdiv.firstChild);
                remove_index--;
            }
        }
//        for (var key in data){ key_arr[key] = key; }
//        for (var i = key_arr.length - 1; i >= 0 ; i--) {
//             ndiv = document.createElement('div');
//             ndiv.innerHTML = `<h2> ${data[i]['title']} </h2><p> ${data[i]['content']}</p><hr>`;
//             pdiv = document.getElementById('newsfeed');
//             pdiv.appendChild(ndiv);
//             skip_index += 1;
//             remove_index += 1;
//             while(remove_index > 10){
//                 pdiv.removeChild(pdiv.lastChild);
//                 remove_index--;
//             }
//        }

//        if(skip_index == 0){
//            for (var key in data){ key_arr[key] = key; }
//            for (var i = key_arr.length - 1; i >= 0 ; i--) {
//                ndiv = document.createElement('div');
//                ndiv.innerHTML = `<h2> ${data[i]['title']} </h2><p> ${data[i]['content']}</p><hr>`;
//                pdiv = document.getElementById('notes');
//                pdiv.appendChild(ndiv);
//                skip_index += 1;
//                remove_index += 1;
//                while(remove_index > 10){
//                    pdiv.removeChild(pdiv.lastChild);
//                    remove_index--;
//                }
//            }
//        }else {
//             for (var key in data){
//                 ndiv = document.createElement('div');
//                 ndiv.innerHTML = `<h2> ${data[key]['title']} </h2><p> ${data[key]['content']}</p><hr>`;
//                 pdiv = document.getElementById('newsfeed');
//                 pdiv.appendChild(ndiv);
//                 skip_index += 1;
//            }
//        }

    } else {
        console.log(`${response.statusText}: ${response.status} error`);
    }
  } catch (error) {
        console.log(error);
  }
}

fetchint = setInterval(fetchRequestWithError, 10 * 100);
