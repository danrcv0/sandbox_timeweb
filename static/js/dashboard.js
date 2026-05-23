
function openTab(id,el){
    document.querySelectorAll('.section').forEach(s=>{
        s.classList.remove('active')
    })

    setTimeout(()=>{
        document.getElementById(id).classList.add('active')
    },50)

    document.querySelectorAll('.menu a').forEach(a=>{
        a.classList.remove('active')
    })

    el.classList.add('active')

}

function toggleMenu(){
    document.getElementById('sidebar').classList.toggle('open')
}

function openModal(contactModel){
    document.getElementById(contactModel).style.display="flex"
}

function closeModal(contactModel){
    document.getElementById(contactModel).style.display="none"
}

function openDetails(meetingId){
    document.getElementById(meetingId).style.display="flex"
}

function closeDetails(meetingId){
    document.getElementById(meetingId).style.display="none"
}

window.onclick=function(event){

    let contact=document.getElementById("contactModal")
    let details=document.getElementById("detailsModal")

    if(event.target==contact){
        contact.style.display="none"
    }

    if(event.target==details){
        details.style.display="none"
    }

}
