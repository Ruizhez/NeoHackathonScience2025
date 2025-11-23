import { useRef } from 'react';
import { motion, useMotionValue } from 'framer-motion';

interface MagneticButtonProps {
  children: React.ReactNode;
  className?: string;
  onClick?: () => void;
  secondary?: boolean;
  disabled?: boolean;
  danger?: boolean;
}

export const MagneticButton = ({
  children,
  className = '',
  onClick,
  secondary = false,
  disabled = false,
  danger = false,
}: MagneticButtonProps) => {
  const ref = useRef<HTMLButtonElement>(null);
  const x = useMotionValue(0);
  const y = useMotionValue(0);

  const handleMouseMove = (e: React.MouseEvent) => {
    if (disabled || !ref.current) return;
    const { clientX, clientY } = e;
    const { left, top, width, height } = ref.current.getBoundingClientRect();
    const centerX = left + width / 2;
    const centerY = top + height / 2;
    x.set((clientX - centerX) * 0.3);
    y.set((clientY - centerY) * 0.3);
  };

  const handleMouseLeave = () => {
    x.set(0);
    y.set(0);
  };

  let borderColor = 'border-white';
  let textColor = 'text-black';
  let bgColor = 'bg-white';
  let hoverBg = 'hover:bg-gray-200';

  if (secondary) {
    borderColor = 'border-white/20';
    textColor = 'text-white';
    bgColor = 'bg-transparent';
    hoverBg = 'hover:bg-white/10';
  } else if (danger) {
    borderColor = 'border-red-500';
    textColor = 'text-red-500';
    bgColor = 'bg-transparent';
    hoverBg = 'hover:bg-red-500/10';
  } else if (disabled) {
    borderColor = 'border-gray-700';
    textColor = 'text-gray-700';
    bgColor = 'bg-transparent';
    hoverBg = 'cursor-not-allowed';
  }

  return (
    <motion.button
      ref={ref}
      disabled={disabled}
      onClick={onClick}
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave}
      style={{ x, y }}
      whileHover={!disabled ? { scale: 1.05 } : {}}
      whileTap={!disabled ? { scale: 0.95 } : {}}
      className={`relative overflow-hidden px-6 py-3 font-bold font-mono uppercase tracking-widest text-[10px] transition-colors border ${borderColor} ${textColor} ${bgColor} ${hoverBg} ${className}`}
    >
      {children}
    </motion.button>
  );
};
