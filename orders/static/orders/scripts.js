const menuColumns = 3;
document.addEventListener('DOMContentLoaded', () => {
  console.log('hello');
  var menuList = document.getElementsByClassName('nav-item');

  Array.from(menuList).forEach(renderMenu);

  function renderMenu (li) {
    li.onclick = () => {
      const request = new XMLHttpRequest();

      request.open('POST', 'get_menu');
      request.responseType = 'json';

      let data = new FormData();
      data.append('name', li.innerText);
      console.log(data.name);

      request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));

      request.send(data);

      request.onload = () => {
        let menuBoard = document.querySelector('#menu-board')
        while (menuBoard.hasChildNodes()) {
            menuBoard.removeChild(menuBoard.firstChild);
        }
        const data = request.response;
        console.log(data);
        console.log(data.menu[1][0]);
        console.log(data.menu[0].length);
        if (data.menu[0].length ===3) {
          let row = '<tr><th></th><th>Small</th><th>Large</th></tr>';
          document.querySelector('#menu-board').innerHTML = row;
        }
        for (let i = 0; i < data.menu.length; i++){
          let newTr = document.createElement('tr');
          for (let j = 0; j < data.menu[0].length; j++){
            let newTd = document.createElement('td');
            // newTd.innerHTML = '<a href=#>' + data.menu[i][j] + '</a>';
            newTd.innerHTML = data.menu[i][j];
            newTr.appendChild(newTd);
          }

          document.querySelector('#menu-board').appendChild(newTr);
        }
        if (data.toppings) {
          let count = 0;
          let length = Math.ceil(data.toppings.length/menuColumns);
          for (let i = 0; i < length; i++){
            let newTr = document.createElement('tr');
            for (let j = 0; j < menuColumns; j++){
              let newTd = document.createElement('td');
              // newTd.innerHTML = '<a href=#>' + data.menu[i][j] + '</a>';
              newTd.innerHTML = data.toppings[count];
              newTr.appendChild(newTd);
              count += 1;
              if (count == data.toppings.length) break;
            }
            document.querySelector('#menu-board').appendChild(newTr);
          }
        }
      };

      // console.log(li.innerText);
      //document.querySelector('.board').innerHTML = data[0].name;
    }
  }

  // function to provide the CSRF protection
  // https://docs.djangoproject.com/en/2.2/ref/csrf/#ajax
  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
  }
  var csrftoken = getCookie('csrftoken');

});
