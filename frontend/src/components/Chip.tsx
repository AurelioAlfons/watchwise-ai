interface ChipProps {
  label: string;
  selected: boolean;
  onClick: () => void;
}

export default function Chip({ label, selected, onClick }: ChipProps) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={`px-4 py-2 rounded-full text-sm font-medium border transition-colors
        ${
          selected
            ? "bg-gold text-ink border-gold"
            : "bg-surfaceSoft text-muted border-border hover:border-gold/50 hover:text-gold"
        }`}
    >
      {label}
    </button>
  );
}