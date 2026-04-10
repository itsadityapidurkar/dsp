"use client";

type SelectProps = {
  value?: string;
  onChange?: (value: string) => void;
  options: string[];
  placeholder?: string;
};


export function Select({ value, onChange, options, placeholder = "Select an option" }: SelectProps) {
  return (
    <select
      value={value ?? ""}
      onChange={(event) => onChange?.(event.target.value)}
      className="w-full rounded-2xl border border-border bg-background px-4 py-3 text-sm"
    >
      <option value="">{placeholder}</option>
      {options.map((option) => (
        <option key={option} value={option}>
          {option}
        </option>
      ))}
    </select>
  );
}
