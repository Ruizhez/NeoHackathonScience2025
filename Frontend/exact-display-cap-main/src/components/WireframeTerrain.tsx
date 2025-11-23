import { useEffect, useRef } from 'react';

const project3D = (x: number, y: number, z: number, width: number, height: number) => {
  const fov = 300;
  const scale = fov / (fov + z);
  const x2d = x * scale + width / 2;
  const y2d = y * scale + height / 2;
  return { x: x2d, y: y2d, scale };
};

export const WireframeTerrain = () => {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    if (!ctx) return;
    
    let animationFrameId: number;
    let time = 0;

    const render = () => {
      time += 0.005;
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
      const w = canvas.width;
      const h = canvas.height;

      ctx.fillStyle = '#050505';
      ctx.fillRect(0, 0, w, h);
      
      const cols = 40;
      const rows = 40;
      const spacing = 60;
      
      const getZ = (i: number, j: number, t: number) => {
        const x = (i - cols/2) * 0.5;
        const y = (j - rows/2) * 0.5;
        const wave1 = Math.sin(x * 0.3 + t) * Math.cos(y * 0.3 + t) * 150;
        const wave2 = Math.sin(Math.sqrt(x*x + y*y) * 0.5 - t * 2) * 100;
        const peakX = -5;
        const peakY = -5;
        const dist = Math.sqrt((x - peakX)**2 + (y - peakY)**2);
        const mountain = Math.exp(-dist * 0.15) * 400;
        return wave1 + wave2 + mountain; 
      };

      ctx.strokeStyle = 'rgba(255, 255, 255, 0.12)';
      ctx.lineWidth = 1;

      for (let j = 0; j < rows; j++) {
        ctx.beginPath();
        for (let i = 0; i < cols; i++) {
          const x = (i - cols / 2) * spacing;
          const z = (j - rows / 2) * spacing + 800; 
          const y = -300 - getZ(i, j, time);
          const p = project3D(x, y, z, w, h);
          if (i === 0) ctx.moveTo(p.x, p.y);
          else ctx.lineTo(p.x, p.y);
        }
        ctx.stroke();
      }

      for (let i = 0; i < cols; i++) {
        ctx.beginPath();
        for (let j = 0; j < rows; j++) {
          const x = (i - cols / 2) * spacing;
          const z = (j - rows / 2) * spacing + 800;
          const y = -300 - getZ(i, j, time);
          const p = project3D(x, y, z, w, h);
          if (j === 0) ctx.moveTo(p.x, p.y);
          else ctx.lineTo(p.x, p.y);
        }
        ctx.stroke();
      }

      ctx.fillStyle = 'rgba(255, 255, 255, 0.4)';
      for (let i = 0; i < cols; i+=2) {
        for (let j = 0; j < rows; j+=2) {
           const x = (i - cols / 2) * spacing;
           const z = (j - rows / 2) * spacing + 800;
           const y = 300; 
           const p = project3D(x, y, z, w, h);
           if (p.scale > 0) ctx.fillRect(p.x, p.y, 1.5 * p.scale, 1.5 * p.scale);
        }
      }

      animationFrameId = requestAnimationFrame(render);
    };
    
    render();
    
    const resize = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };
    
    window.addEventListener('resize', resize);
    
    return () => {
      window.removeEventListener('resize', resize);
      cancelAnimationFrame(animationFrameId);
    };
  }, []);

  return <canvas ref={canvasRef} className="fixed inset-0 z-0 pointer-events-none opacity-60" />;
};
