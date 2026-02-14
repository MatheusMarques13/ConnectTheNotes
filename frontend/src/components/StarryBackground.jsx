import React, { useEffect, useRef } from 'react';

const StarryBackground = () => {
  const canvasRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    let animationId;
    let stars = [];
    let constellations = [];
    let shootingStars = [];

    const resize = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
      initStars();
      initConstellations();
    };

    const initStars = () => {
      stars = [];
      const count = Math.floor((canvas.width * canvas.height) / 3000);
      for (let i = 0; i < count; i++) {
        stars.push({
          x: Math.random() * canvas.width,
          y: Math.random() * canvas.height,
          radius: Math.random() * 1.5 + 0.3,
          opacity: Math.random() * 0.8 + 0.2,
          twinkleSpeed: Math.random() * 0.02 + 0.005,
          twinkleOffset: Math.random() * Math.PI * 2,
        });
      }
    };

    const initConstellations = () => {
      constellations = [];
      const numConstellations = 12;
      for (let i = 0; i < numConstellations; i++) {
        const cx = Math.random() * canvas.width;
        const cy = Math.random() * canvas.height;
        const numPoints = Math.floor(Math.random() * 5) + 4;
        const points = [];
        for (let j = 0; j < numPoints; j++) {
          points.push({
            x: cx + (Math.random() - 0.5) * 250,
            y: cy + (Math.random() - 0.5) * 200,
          });
        }
        const connections = [];
        for (let j = 0; j < points.length - 1; j++) {
          connections.push([j, j + 1]);
        }
        if (points.length > 3 && Math.random() > 0.5) {
          connections.push([0, Math.floor(points.length / 2)]);
        }
        constellations.push({ points, connections, opacity: Math.random() * 0.15 + 0.05 });
      }
    };

    const spawnShootingStar = () => {
      if (Math.random() < 0.002 && shootingStars.length < 2) {
        shootingStars.push({
          x: Math.random() * canvas.width,
          y: Math.random() * canvas.height * 0.3,
          vx: (Math.random() - 0.3) * 8,
          vy: Math.random() * 4 + 2,
          life: 1,
          length: Math.random() * 60 + 40,
        });
      }
    };

    const draw = (time) => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      // Draw constellations
      constellations.forEach(constellation => {
        const { points, connections, opacity } = constellation;
        ctx.strokeStyle = `rgba(196, 163, 90, ${opacity})`;
        ctx.lineWidth = 0.7;
        connections.forEach(([a, b]) => {
          ctx.beginPath();
          ctx.moveTo(points[a].x, points[a].y);
          ctx.lineTo(points[b].x, points[b].y);
          ctx.stroke();
        });
        points.forEach(p => {
          ctx.beginPath();
          ctx.arc(p.x, p.y, 2, 0, Math.PI * 2);
          ctx.fillStyle = `rgba(196, 163, 90, ${opacity + 0.15})`;
          ctx.fill();
        });
      });

      // Draw stars
      stars.forEach(star => {
        const twinkle = Math.sin(time * star.twinkleSpeed + star.twinkleOffset) * 0.3 + 0.7;
        ctx.beginPath();
        ctx.arc(star.x, star.y, star.radius, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(196, 163, 90, ${star.opacity * twinkle})`;
        ctx.fill();
      });

      // Draw shooting stars
      spawnShootingStar();
      shootingStars = shootingStars.filter(s => s.life > 0);
      shootingStars.forEach(s => {
        s.x += s.vx;
        s.y += s.vy;
        s.life -= 0.015;
        const gradient = ctx.createLinearGradient(
          s.x, s.y,
          s.x - s.vx * (s.length / 8), s.y - s.vy * (s.length / 8)
        );
        gradient.addColorStop(0, `rgba(255, 255, 255, ${s.life})`);
        gradient.addColorStop(1, 'rgba(255, 255, 255, 0)');
        ctx.strokeStyle = gradient;
        ctx.lineWidth = 1.5;
        ctx.beginPath();
        ctx.moveTo(s.x, s.y);
        ctx.lineTo(s.x - s.vx * (s.length / 8), s.y - s.vy * (s.length / 8));
        ctx.stroke();
      });

      animationId = requestAnimationFrame(draw);
    };

    resize();
    animationId = requestAnimationFrame(draw);
    window.addEventListener('resize', resize);

    return () => {
      cancelAnimationFrame(animationId);
      window.removeEventListener('resize', resize);
    };
  }, []);

  return (
    <canvas
      ref={canvasRef}
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        width: '100%',
        height: '100%',
        pointerEvents: 'none',
        zIndex: 0,
      }}
    />
  );
};

export default StarryBackground;
