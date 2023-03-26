document.addEventListener("DOMContentLoaded", function () {
    const simplemde = new SimpleMDE({element: document.getElementById("markdown-editor")});
});
document.addEventListener("DOMContentLoaded", function () {
    new ClipboardJS('.copy-btn');
});