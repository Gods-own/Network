let editBtns = document.getElementsByClassName('edit')
Array.prototype.forEach.call(editBtns, function(editbtn) {
    editbtn.addEventListener('click', function(e){
        e.stopImmediatePropagation()
        let postid;
        let str = editbtn.dataset.id 
        strlen = str.length - 4
                
        postid = str.substring(0, strlen)
        editpost(postid)  
        document.querySelector(`[data-id="image-icon${postid}"]`).addEventListener('click', function(e) {
            e.stopImmediatePropagation()
            document.querySelector(`[data-id="image-form${postid}"]`).classList.toggle('show');
        })
    })
})

function editpost(postid) {
    document.querySelector(`[data-id="card${postid}"]`).classList.toggle('hide')
    document.querySelector(`[data-id="form${postid}"]`).classList.toggle('show')
    document.querySelector(`[data-id="form${postid}"]`).addEventListener('submit', function(e) {
        e.preventDefault()
        e.stopImmediatePropagation()
        savepost(postid)
        document.querySelector(`[data-id="card${postid}"]`).classList.remove('hide')
        document.querySelector(`[data-id="form${postid}"]`).classList.remove('show')
    })
}

function savepost(postid) {
    let editedpost = document.querySelector(`[data-id="text${postid}"]`).value
    let editedpicture = document.querySelector(`[data-id="image${postid}"]`).value;
    if (editedpicture.trim()) {
        editedpicture = document.querySelector(`[data-id="image${postid}"]`).value
    }
    else {
        editedpicture = null;
    }
    fetch("/editpost/"+postid, {
        method: 'PUT',
        body: JSON.stringify({
            post_id: postid,
            post: editedpost,
            picture: editedpicture
        })
    })
    .then(response => response.json())
    .then(data => {
        return getpost(postid)
    })
}

function getpost(postid) {
    fetch("/editpost/"+postid)
    .then(response => response.json())
    .then(data => {
        document.querySelector(`[data-id="${postid}post"]`).innerHTML = `${data.post}`
        if ('picture' in data) {
            document.querySelector(`[data-id="${postid}image"]`).innerHTML = `${data.picture}`
        }
    })
}