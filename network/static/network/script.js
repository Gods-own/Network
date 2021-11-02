document.addEventListener("DOMContentLoaded", function() { 

    // Selecting the element containing the like and unlike buttons
    let likeBtns = document.getElementsByClassName('like-buttons')    
    Array.prototype.forEach.call(likeBtns, function(likeBtn) {
        let postid = likeBtn.dataset.id
        checklike(postid)
    })

    // Selecting the like button and giving it a function to like a post
    let uncoloredBtns = document.querySelectorAll('.uncolored-heart')
    Array.prototype.forEach.call(uncoloredBtns, function(likeBtn) {
        likeBtn.addEventListener('click', function() {
                color = "white"
                let postid;
                let str = likeBtn.dataset.id 
                strlen = str.length - 9
                
                postid = str.substring(0, strlen)
                likepost(postid, color)
        })
    })
    
    // Selecting the like button and giving it a function to unlike a post
    let coloredBtns = document.querySelectorAll('.colored-heart')
    Array.prototype.forEach.call(coloredBtns, function(likeBtn) {
        likeBtn.addEventListener('click', function() {
            color = "red"
            let postid;
            let str = likeBtn.dataset.id 
            strlen = str.length - 7
                
            postid = str.substring(0, strlen)
            likepost(postid, color)
        })
    })
    
})

// function to like and unlike a post
function likepost(postid, color) {
    fetch("/like/"+postid, {
        method: 'PUT',
        body: JSON.stringify({
            post_id: postid
        })
    })
    .then(response => response.json())
    .then(data => {
        return getlike(postid, color)
    })
}

// function to get the number of likes a post has
function getlike(postid, color) {
    fetch("/like/"+postid)
    .then(response => response.json())
    .then(data => {
        if (color == "red") {
            document.querySelector(`[data-id="${postid}uncolored"]`).classList.toggle('hide')
            document.querySelector(`[data-id="${postid}colored"]`).classList.toggle('show-inline')
        }
        else {
            document.querySelector(`[data-id="${postid}colored"]`).classList.toggle('show-inline')
            document.querySelector(`[data-id="${postid}uncolored"]`).classList.toggle('hide')
        }
        document.querySelector(`#like${postid}`).innerHTML = data.like
    })
}

// function to check if a post is like by the logged in user
function checklike(postid) {
    fetch("/isliked/"+postid)
    .then(response => response.json())
    .then(data => {
        let uncolored = `[data-id="${postid}uncolored"]`
        let colored = `[data-id="${postid}colored"]`
        if (data.liked == true) {
            document.querySelector(uncolored).classList.add('hide')
            document.querySelector(colored).classList.add('show-inline')
        } 
    })
}

