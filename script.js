'use strict';
const menuButton = document.querySelector('.menu-toggle');
const navigation = document.querySelector('#navigation');
menuButton.addEventListener('click', () => {
  const expanded = menuButton.getAttribute('aria-expanded') === 'true';
  menuButton.setAttribute('aria-expanded', String(!expanded));
  navigation.classList.toggle('open', !expanded);
});
navigation.querySelectorAll('a').forEach(link => link.addEventListener('click', () => {
  menuButton.setAttribute('aria-expanded', 'false');
  navigation.classList.remove('open');
}));
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && navigation.classList.contains('open')) {
    menuButton.setAttribute('aria-expanded', 'false');
    navigation.classList.remove('open');
    menuButton.focus();
  }
});
const cards = [...document.querySelectorAll('.project-card')];
document.querySelectorAll('.filter').forEach(button => button.addEventListener('click', () => {
  document.querySelectorAll('.filter').forEach(filter => {
    const selected = filter === button;
    filter.classList.toggle('active', selected);
    filter.setAttribute('aria-pressed', String(selected));
  });
  cards.forEach(card => { card.hidden = button.dataset.filter !== 'all' && card.dataset.category !== button.dataset.filter; });
  const count = cards.filter(card => !card.hidden).length;
  document.querySelector('#filter-status').textContent = `${count} ${count === 1 ? 'project' : 'projects'} shown`;
}));
document.querySelector('#year').textContent = new Date().getFullYear();
let toastTimeout;
document.querySelector('#copy-email').addEventListener('click', async () => {
  const toast = document.querySelector('#toast');
  try {
    await navigator.clipboard.writeText('ehtishamfazal68@gmail.com');
    toast.textContent = 'Email address copied';
  } catch {
    toast.textContent = 'Email: ehtishamfazal68@gmail.com';
  }
  toast.classList.add('show');
  clearTimeout(toastTimeout);
  toastTimeout = setTimeout(() => toast.classList.remove('show'), 3500);
});

// A lightweight original canvas drawing; no 3D library or downloaded scene.
const canvas = document.querySelector('#neural-canvas');
const ctx = canvas.getContext('2d');
if (ctx) {
  const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
  let paused = reducedMotion.matches;
  let visible = true;
  let width = 0, height = 0, rotation = .35, frame = 0;
  let pointerX = 0, pointerY = 0;
  const nodes = Array.from({ length: 150 }, (_, index) => {
    const y = 1 - index / 149 * 2;
    const radius = Math.sqrt(1 - y * y);
    const theta = index * Math.PI * (3 - Math.sqrt(5));
    return { x: Math.cos(theta) * radius, y, z: Math.sin(theta) * radius };
  });
  const edges = [];
  nodes.forEach((a, i) => nodes.slice(i + 1).forEach((b, offset) => {
    const distance = Math.hypot(a.x-b.x, a.y-b.y, a.z-b.z);
    if (distance < .39) edges.push([i, i + offset + 1]);
  }));
  function resize() {
    const rect = canvas.getBoundingClientRect();
    width = rect.width; height = rect.height;
    const ratio = Math.min(devicePixelRatio || 1, 2);
    canvas.width = width * ratio; canvas.height = height * ratio;
    ctx.setTransform(ratio, 0, 0, ratio, 0, 0);
    draw();
  }
  function draw() {
    ctx.clearRect(0, 0, width, height);
    const size = Math.min(width * .32, height * .43);
    const angle = rotation + pointerX * .16;
    const tilt = -.22 + pointerY * .12;
    const projected = nodes.map(node => {
      const x = node.x * Math.cos(angle) - node.z * Math.sin(angle);
      const z = node.x * Math.sin(angle) + node.z * Math.cos(angle);
      const y = node.y * Math.cos(tilt) - z * Math.sin(tilt);
      const depth = node.y * Math.sin(tilt) + z * Math.cos(tilt);
      const perspective = 3.4 / (3.4 - depth);
      return { x: width / 2 + x * size * perspective, y: height / 2 + y * size * perspective - 8, depth };
    });
    // Fine orbital ellipses anchor the network without visual clutter.
    ctx.save(); ctx.translate(width/2, height/2 - 8); ctx.rotate(-.4);
    ctx.beginPath(); ctx.ellipse(0, 0, size*1.4, size*.38, 0, 0, Math.PI*2);
    ctx.strokeStyle = '#8ca88940'; ctx.lineWidth = .7; ctx.stroke(); ctx.restore();
    edges.forEach(([i,j]) => {
      const a = projected[i], b = projected[j];
      const alpha = .06 + ((a.depth + b.depth + 2) / 4) * .28;
      ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y);
      ctx.strokeStyle = `rgba(65,111,76,${alpha})`; ctx.lineWidth = .7; ctx.stroke();
    });
    projected.sort((a,b) => a.depth - b.depth).forEach((node, i) => {
      const alpha = .24 + (node.depth + 1) / 2 * .65;
      ctx.beginPath(); ctx.arc(node.x, node.y, (node.depth + 2) * .85, 0, Math.PI*2);
      ctx.fillStyle = `rgba(48,101,66,${alpha})`; ctx.fill();
      if (i % 31 === 0) { ctx.beginPath(); ctx.arc(node.x,node.y,5,0,Math.PI*2);ctx.strokeStyle='#6a956d40';ctx.stroke(); }
    });
  }
  function animate() {
    if (paused || !visible || document.hidden) { frame = 0; return; }
    rotation += .0022; draw(); frame = requestAnimationFrame(animate);
  }
  function syncMotion() {
    document.querySelector('#motion-toggle').textContent = paused ? 'Play motion' : 'Pause motion';
    document.querySelector('#motion-toggle').setAttribute('aria-pressed', String(paused));
    if (!frame) animate();
  }
  document.querySelector('#motion-toggle').addEventListener('click', () => { paused = !paused; syncMotion(); });
  reducedMotion.addEventListener('change', event => { paused = event.matches; syncMotion(); });
  canvas.addEventListener('pointermove', event => {
    if (paused) return;
    const rect = canvas.getBoundingClientRect();
    pointerX = (event.clientX - rect.left) / width - .5;
    pointerY = (event.clientY - rect.top) / height - .5;
  });
  canvas.addEventListener('pointerleave', () => { pointerX = 0; pointerY = 0; });
  new ResizeObserver(resize).observe(canvas);
  new IntersectionObserver(entries => { visible = entries[0].isIntersecting; if (visible && !frame) animate(); }).observe(canvas);
  document.addEventListener('visibilitychange', () => { if (!document.hidden && !frame) animate(); });
  resize(); syncMotion();
}
