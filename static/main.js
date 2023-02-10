let tabMap=[['price','priceTable'],['month revenue','revenueTable'],['statement sheet','financialTable'],['dividend','dividendTable']]

// Get the element with id="defaultOpen" and click on it
document.getElementById("defaultOpen").click();
showPage()
createAllContent()

function showPage() {
    document.getElementById("loader").style.display = "none";
    document.getElementById("overlay").style.display = "none";
}
function loadingPage(){
    document.getElementById("overlay").style.display = "block";
    document.getElementById("loader").style.display = "block"
}

function createTable(tabName,data){
    let tableContent=document.getElementById(tabName+" -table")
    tableContent.innerHTML=''
    let thead=document.createElement("thead")
    let theadTr=document.createElement("tr")
    let tbody=document.createElement("tbody")
    thead.appendChild(theadTr)
    tableContent.appendChild(thead)
    tableContent.appendChild(tbody)
    const okeys = Object.keys(data)
    const ovalues = Object.values(data)
    
    for (i=0;i<okeys.length;i++){
        let trTh=document.createElement('th')
        trTh.textContent=okeys[i]
        theadTr.appendChild(trTh)
    }
    for (i=0;i<Object.keys(ovalues[0]).length;i++){
        let tbodyTr=document.createElement('tr')
        tbody.appendChild(tbodyTr)
        for (j=0;j<okeys.length;j++){
            let trTd=document.createElement('td')
            trTd.textContent=ovalues[j][i]
            tbodyTr.appendChild(trTd)
        }
    }   
}

// function createContent(url="/table/",tabName="") {
//     loadingPage()
//     let stockId=""
//     if(tabName==""){
//         stockId = document.getElementById('stockId').value;
//         console.log('request single data')
//     }else{
//         console.log('request multi data')
//     }

//     fetch(url+stockId).then(function (response) {
//         return response.json()
//     }).then(function (data) {
//         if(tabName==""){
//             // console.log("get all single data",data)
//             for(let i=0;i<tabMap.length;i++){
//                 console.log("table",tabMap[i][1])
//                 let data1={...JSON.parse(data[tabMap[i][1]])}
//                 createTable(tabMap[i][0],data1)
//             }
//         }
//         else{
//             console.log("get multi data",data)
//             createTable(tabName,data)
//         }
//         showPage()
//     })
// }
function getApi(url){
    loadingPage()
    return fetch(url)
    .then((response)=>response.json())
    .then((data)=>{
        showPage()
        console.log("call url",url)
        console.log("print data",data)
        return data
    })    
}
async function createContent(){
    stockId = document.getElementById('stockId').value;
    let data= await getApi('/table/'+stockId)    

    for(let i=0;i<tabMap.length;i++){
        console.log("table",tabMap[i][1])
        let data1={...JSON.parse(data[tabMap[i][1]])}
        createTable(tabMap[i][0],data1)
    }
    return data
}
function createAllContent(){
    createContent().then(()=>{
        console.log('complete')
        getApi('/overview')
    })
    // createContent("/overview","overview")
}
function openContent(evt, tabName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
}