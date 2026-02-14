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
    let mouseX = -1000;
    let mouseY = -1000;

    const resize = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
      initStars();
      initConstellations();
    };

    const handleMouseMove = (e) => {
      mouseX = e.clientX;
      mouseY = e.clientY;
    };

    const initStars = () => {
      stars = [];
      const count = Math.floor((canvas.width * canvas.height) / 2500);
      for (let i = 0; i < count; i++) {
        stars.push({
          x: Math.random() * canvas.width,
          y: Math.random() * canvas.height,
          radius: Math.random() * 1.3 + 0.2,
          opacity: Math.random() * 0.7 + 0.15,
          twinkleSpeed: Math.random() * 0.015 + 0.003,
          twinkleOffset: Math.random() * Math.PI * 2,
          // Color variation: icy blues, silvers, and white
          hue: Math.random() > 0.6 ? 220 + Math.random() * 20 : 210 + Math.random() * 40,
          saturation: Math.random() * 30 + 10,
          lightness: Math.random() * 20 + 75,
        });
      }
    };

    const initConstellations = () => {
      constellations = [];
      const numConstellations = 14;
      for (let i = 0; i < numConstellations; i++) {
        const cx = Math.random() * canvas.width;
        const cy = Math.random() * canvas.height;
        const numPoints = Math.floor(Math.random() * 5) + 3;
        const points = [];
        for (let j = 0; j < numPoints; j++) {
          points.push({
            x: cx + (Math.random() - 0.5) * 280,
            y: cy + (Math.random() - 0.5) * 220,
          });
        }
        const connections = [];
        for (let j = 0; j < points.length - 1; j++) {
          connections.push([j, j + 1]);
        }
        if (points.length > 3 && Math.random() > 0.4) {
          connections.push([0, Math.floor(points.length / 2)]);
        }
        if (points.length > 4 && Math.random() > 0.6) {
          connections.push([1, points.length - 1]);
        }
        constellations.push({ 
          points, 
          connections, 
          opacity: Math.random() * 0.1 + 0.03,
          baseOpacity: Math.random() * 0.1 + 0.03,
        });
      }
    };

    const spawnShootingStar = () => {
      if (Math.random() < 0.0015 && shootingStars.length < 2) {
        shootingStars.push({
          x: Math.random() * canvas.width * 0.8,
          y: Math.random() * canvas.height * 0.2,
          vx: (Math.random() * 4 + 3),
          vy: Math.random() * 2 + 1,
          life: 1,
          length: Math.random() * 80 + 50,
        });
      }
    };

    const draw = (time) => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      // Draw constellations with mouse proximity glow
      constellations.forEach(constellation => {
        const { points, connections, baseOpacity } = constellation;
        
        // Check mouse proximity to constellation center
        let centerX = 0, centerY = 0;
        points.forEach(p => { centerX += p.x; centerY += p.y; });
        centerX /= points.length;
        centerY /= points.length;
        const dist = Math.sqrt((mouseX - centerX) ** 2 + (mouseY - centerY) ** 2);
        const proximity = Math.max(0, 1 - dist / 400);
        const dynamicOpacity = baseOpacity + proximity * 0.12;

        // Draw lines
        ctx.strokeStyle = `rgba(163, 191, 250, ${dynamicOpacity})`;
        ctx.lineWidth = 0.6;
        connections.forEach(([a, b]) => {
          ctx.beginPath();
          ctx.moveTo(points[a].x, points[a].y);
          ctx.lineTo(points[b].x, points[b].y);
          ctx.stroke();
        });

        // Draw constellation nodes
        points.forEach(p => {
          const nodeDist = Math.sqrt((mouseX - p.x) ** 2 + (mouseY - p.y) ** 2);
          const nodeGlow = Math.max(0, 1 - nodeDist / 250);
          const nodeSize = 1.8 + nodeGlow * 2;
          
          ctx.beginPath();
          ctx.arc(p.x, p.y, nodeSize, 0, Math.PI * 2);
          ctx.fillStyle = `rgba(184, 198, 224, ${dynamicOpacity + 0.1 + nodeGlow * 0.3})`;
          ctx.fill();

          // Diamond sparkle on close nodes
          if (nodeGlow > 0.3) {
            ctx.beginPath();
            ctx.arc(p.x, p.y, nodeSize + 4, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(199, 210, 254, ${nodeGlow * 0.08})`;
            ctx.fill();
          }
        });
      });

      // Draw stars with twinkle
      stars.forEach(star => {
        const twinkle = Math.sin(time * star.twinkleSpeed + star.twinkleOffset) * 0.35 + 0.65;
        
        // Mouse proximity effect
        const dist = Math.sqrt((mouseX - star.x) ** 2 + (mouseY - star.y) ** 2);
        const proximity = Math.max(0, 1 - dist / 200);
        const finalOpacity = star.opacity * twinkle + proximity * 0.3;
        const finalRadius = star.radius + proximity * 0.8;
        
        ctx.beginPath();
        ctx.arc(star.x, star.y, finalRadius, 0, Math.PI * 2);
        ctx.fillStyle = `hsla(${star.hue}, ${star.saturation}%, ${star.lightness}%, ${finalOpacity})`;
        ctx.fill();
      });

      // Draw shooting stars
      spawnShootingStar();
      shootingStars = shootingStars.filter(s => s.life > 0);
      shootingStars.forEach(s => {
        s.x += s.vx;
        s.y += s.vy;
        s.life -= 0.012;
        const gradient = ctx.createLinearGradient(
          s.x, s.y,
          s.x - s.vx * (s.length / 8), s.y - s.vy * (s.length / 8)
        );
        gradient.addColorStop(0, `rgba(212, 223, 245, ${s.life * 0.9})`);
        gradient.addColorStop(0.4, `rgba(163, 191, 250, ${s.life * 0.5})`);
        gradient.addColorStop(1, 'rgba(163, 191, 250, 0)');
        ctx.strokeStyle = gradient;
        ctx.lineWidth = 1.2;
        ctx.beginPath();
        ctx.moveTo(s.x, s.y);
        ctx.lineTo(s.x - s.vx * (s.length / 8), s.y - s.vy * (s.length / 8));
        ctx.stroke();

        // Head glow
        ctx.beginPath();
        ctx.arc(s.x, s.y, 2, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(232, 238, 255, ${s.life * 0.6})`;
        ctx.fill();
      });

      animationId = requestAnimationFrame(draw);
    };

    resize();
    animationId = requestAnimationFrame(draw);
    window.addEventListener('resize', resize);
    window.addEventListener('mousemove', handleMouseMove);

    return () => {
      cancelAnimationFrame(animationId);
      window.removeEventListener('resize', resize);
      window.removeEventListener('mousemove', handleMouseMove);
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
