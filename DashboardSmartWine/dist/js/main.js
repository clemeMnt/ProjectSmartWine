
var db = firebase.firestore();
const auth = firebase.auth();

auth.onAuthStateChanged(user => {
  if (user) {
    var usr = user.uid;
    getdata(usr);
    getdataSensor();
  } else {
    window.location.replace("login.html");
  }
})

const logout = document.querySelector('#logout');
logout.addEventListener('click', (e)=> {
  e.preventDefault();
  auth.signOut().then(() => {
  });
})


function getdata(usr){
  var docRef = db.collection("users").doc(usr);
  docRef.collection("bottle").get().then(snapshot => {
      setupList(snapshot.docs);
  }).catch(function(error) {
      console.log("Error getting document:", error);
  });
   
}

const setupList = (list) =>{
  let html = '';
  list.forEach(doc => {
    const data = doc.data();
    const tr = `
            <tr>
                <td>${data.title}</td>
                <td>${data.designation}</td>
                <td>${data.variety}</td>
                <td>${data.region}</td>
                <td>${data.winery}</td>
            </tr>
            `;
    html += tr;
  });
  document.querySelector('#tbody').innerHTML = html
} 


function getdataSensor(){
  let docRef = db.collection("Cave").doc("1");
  
  docRef.collection('sensor').orderBy("date", "desc").limit(10).get().then(snapshot => {
    setupTemp(snapshot.docs);
  }).catch(function(error) {
      console.log("Error getting document:", error);
  });
     
}

const setupTemp = (list) =>{

  let date = [];
  let temp = [];
  let humid = [];

  list.forEach(doc => {
    const data = doc.data();
    date.push(data.date);
    temp.push(data.temp);
    humid.push(data.humi);
    
  })
  
  date.reverse();
  temp.reverse();
  humid.reverse();

  let configTemp = {
    type: 'line',

    data: {
        labels: date,
        datasets: [{
                label: 'Temperature',
                borderColor: 'rgb(239, 41, 150)',
                backgroundColor: 'rgb(239, 41, 150, 0.2)',
                hoverBackgroundColor: '#ffffff',
                hoverBorderColor: '#ffffff',
                data: temp,
            }],
        fill: false,
    },
    option: {

        responsive: true,
        plugins: {
            title: {
                display: true,
                text: 'Chart.js Line Chart'
            },
            tooltip: {
                mode: 'index',
                intersect: false,
            }
        },
        hover: {
            mode: 'nearest',
            intersect: true
        },
        scales: {
            x: {
                display: true,
            },
            y: {
                display: true,
                min: 0,
                max: 100,
                ticks: {
                    stepSize: 5
                }
            }
        }
    }
  };
  
  let ctxt = document.querySelector('#graphCanvas').getContext('2d');
  window.myLine = new Chart(ctxt, configTemp);

  document.querySelector('#temp').innerHTML = temp[temp.length - 1]+"°C";

  let configHygro = {
    type: 'line',

    data: {
        labels: date,
        datasets: [
            {

                label: 'Hygrometrie',
                borderColor: 'rgb(239, 41, 150)',
                backgroundColor: 'rgb(239, 41, 150, 0.2)',
                hoverBackgroundColor: '#ffffff',
                hoverBorderColor: '#ffffff',
                data: humid
            },
        ],
        fill: false,
    },
    option: {

        responsive: true,
        plugins: {
            title: {
                display: true,
                text: 'Chart.js Line Chart'
            },
            tooltip: {
                mode: 'index',
                intersect: false,
            }
        },
        hover: {
            mode: 'nearest',
            intersect: true
        },
        scales: {
            x: {
                display: true,
            },
            y: {
                display: true,
                min: 0,
                max: 100,
                ticks: {
                    stepSize: 5
                }
            }
        }
    }
  };
  let ctxh = document.getElementById('graphCanvas2').getContext('2d');
  window.myLine = new Chart(ctxh, configHygro);
  document.getElementById('hygro').innerHTML = humid[humid.length - 1] + "%";
  setTimeout(getdataSensor, 50000);

}
