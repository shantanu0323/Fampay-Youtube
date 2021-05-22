async function loadInitialDashboard() {
    console.log("Loading initiated");
    const params = new URLSearchParams(window.location.search)
    var pageNumber = 1
    if (params.has('pageNumber'))
        pageNumber = params.get('pageNumber');
    var maxResults = 10
    if (params.has('maxResults'))
        maxResults = params.get('maxResults');
    let res = await fetch(`/get?pageNumber=${pageNumber}&maxResults=${maxResults}`, {
        method: 'GET'
    });
    let data = await res.json();
    console.log(data);
    if (data["noOfVideos"] == 0) {

    } else {
        data["videos"].forEach(video => {
            videoContainer = document.createElement('div');
            videoContainer.classList.add('video-container');
            videoContainer.setAttribute('id', video["_id"]);
            
            thumbnail = document.createElement('img');
            thumbnail.classList.add("video-thumbnail");
            thumbnail.setAttribute('src', video["thumbnailUrl"]);
            thumbnail.setAttribute('alt', "Thumbnail");

            videoRightContainer = document.createElement('div');
            videoRightContainer.classList.add("video-right-container");

            title = document.createElement('span');
            title.classList.add("video-title");
            title.innerHTML = video["title"];
        
            description = document.createElement('span');
            description.classList.add("video-description");
            description.innerHTML = video["description"];
        
            publishedAt = document.createElement('span');
            publishedAt.classList.add("video-published-at");
            date = new Date(Date.parse(video["publishedAt"]))
            date_str = date.toLocaleString('en-US', {
                weekday: 'short',
                day: 'numeric',
                year: 'numeric',
                month: 'long',
                hour: 'numeric',
                minute: 'numeric',
                second: 'numeric',
            });
            publishedAt.innerHTML = `<span style="font-style: italic; font-size: 0.9em; color: grey;">-- published on</span> ${date_str}`;
        
            youtube = document.createElement('a');
            youtube.classList.add("video-youtube-link");
            youtube.setAttribute('href', `https://www.youtube.com/watch?v=${video["_id"]}`);
            youtube.setAttribute('target', '_blank');
            youtube.innerHTML = "Watch on Youtube";
        
            videoRightContainer.appendChild(title);
            videoRightContainer.appendChild(description);
            videoRightContainer.appendChild(document.createElement('br'));
            videoRightContainer.appendChild(publishedAt);
            videoRightContainer.appendChild(youtube);

            videoContainer.appendChild(thumbnail);
            videoContainer.appendChild(videoRightContainer);

            document.getElementsByClassName("videos-list-container")[0].appendChild(videoContainer);
        });
    }
}

window.onload = function () {
    loadInitialDashboard();
}