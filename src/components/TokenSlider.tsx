import { Sliders } from 'lucide-react';

interface TokenSliderProps {
  tokenCount: number;
  onTokenCountChange: (count: number) => void;
}

export default function TokenSlider({
  tokenCount,
  onTokenCountChange,
}: TokenSliderProps) {
  return (
    <div className="border-4 border-black p-6 bg-white">
      <div className="flex items-center gap-3 mb-4">
        <Sliders size={24} strokeWidth={3} />
        <h2 className="text-2xl font-black">PREFIX LENGTH</h2>
      </div>
      <div className="space-y-4">
        <div className="flex justify-between items-center">
          <span className="font-bold text-lg">Number of Tokens:</span>
          <span className="text-3xl font-black bg-yellow-300 border-4 border-black px-6 py-2">
            {tokenCount}
          </span>
        </div>
        <input
          type="range"
          min="5"
          max="200"
          step="5"
          value={tokenCount}
          onChange={(e) => onTokenCountChange(Number(e.target.value))}
          className="w-full h-4 bg-gray-200 border-4 border-black appearance-none cursor-pointer"
          style={{
            background: `linear-gradient(to right, #FDE047 0%, #FDE047 ${
              ((tokenCount - 5) / 195) * 100
            }%, #E5E7EB ${((tokenCount - 5) / 195) * 100}%, #E5E7EB 100%)`,
          }}
        />
        <div className="flex justify-between text-sm font-bold">
          <span>5 tokens</span>
          <span>200 tokens</span>
        </div>
      </div>
    </div>
  );
}
