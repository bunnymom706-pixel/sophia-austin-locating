/* Injects the Spirit Real Estate Group logo and the Equal Housing Opportunity mark.
   If assets/brand/spirit_logo.png exists (drop the official file there), it is used;
   otherwise the logo is rebuilt from HTML/SVG so the flyer still renders. */
(function () {
  var FLAME =
    '<svg viewBox="0 0 60 100" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">' +
    '<path fill="#F2A93B" d="M31 0c2 14-6 22-12 31C13 40 6 48 6 62c0 21 12 38 26 38 13 0 23-13 23-32 0-12-7-19-11-27-1 8-3 12-7 14 6-12 3-32-6-55z"/>' +
    '<path fill="#FFFFFF" d="M31 56c2 8-3 11-6 16-3 4-6 8-6 13 0 8 5 13 11 13 6 0 10-5 10-12 0-5-3-8-5-12-1 5-2 6-4 7 3-6 2-15 0-25z"/>' +
    '</svg>';

  var EHO =
    '<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg" aria-label="Equal Housing Opportunity">' +
    '<path fill="currentColor" d="M32 4 2 28h8v30h44V28h8L32 4zm0 8.5L47 25v27H17V25l15-12.5z"/>' +
    '<rect fill="currentColor" x="22" y="31" width="20" height="5"/><rect fill="currentColor" x="22" y="41" width="20" height="5"/>' +
    '</svg>';

  function buildLogo(el) {
    var root = el.getAttribute('data-root') || '../../assets/brand/';
    var img = document.createElement('img');
    img.className = 'spirit-logo-img';
    img.alt = 'Spirit Real Estate Group';
    var built = document.createElement('div');
    built.className = 'spirit-built';
    built.hidden = true;
    built.innerHTML =
      '<div class="spirit-word"><span>SPIR</span><span class="i-flame">I' + FLAME + '</span><span>T</span></div>' +
      '<div class="spirit-sub">Real Estate Group</div>';
    img.onerror = function () { img.remove(); built.hidden = false; };
    img.src = root + 'spirit_logo.png';
    el.appendChild(img);
    el.appendChild(built);
  }

  document.querySelectorAll('.spirit-logo').forEach(buildLogo);
  document.querySelectorAll('.eho').forEach(function (el) {
    el.insertAdjacentHTML('afterbegin', EHO);
  });
})();
