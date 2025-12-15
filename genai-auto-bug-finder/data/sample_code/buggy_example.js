
function render(content) {
  document.write(content);
  var x = eval(content);
  document.getElementById('out').innerHTML = content;
}
