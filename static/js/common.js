// htmx.logAll();
// monitorEvents(htmx.find('#rateProblem6363'))

window.addEventListener("scroll", function() {
    const distance = window.scrollY
    const herotext = document.querySelector(".herotext-anim")
    if (herotext) {
        const opacity = 1 - distance / (window.innerHeight * 0.15)
        herotext.style.transform = `translateY(${distance * 0.7}px)`
        herotext.style.opacity = opacity
    }
});

let csrfToken = JSON.parse(
    document.querySelector('body').getAttribute('hx-headers')
)['X-CSRFToken']

function tagifyAction(action, tagName) {
    let formData = new FormData()
    formData.append('tag', tagName)
    fetch(action, {
        method: 'POST',
        body: formData,
        headers: {'X-CSRFToken': csrfToken},
    })
}
