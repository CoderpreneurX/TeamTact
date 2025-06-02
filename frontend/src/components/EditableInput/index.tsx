import { useState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

interface EditableInputProps {
  value: string;
  onSave?: (newValue: string) => void;
  label?: string;
  placeholder?: string;
}

export function EditableInput({ value, onSave = () => {}, label, placeholder }: EditableInputProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [inputValue, setInputValue] = useState(value);

  const handleToggle = () => {
    if (isEditing) {
      onSave(inputValue); // Trigger on save
    }
    setIsEditing(!isEditing);
  };

  return (
    <div className="space-y-1">
      {label && <label className="text-sm font-medium text-gray-700">{label}</label>}
      <div className="flex items-center gap-2">
        <Input
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          disabled={!isEditing}
          placeholder={placeholder}
        />
        <Button variant="outline" onClick={handleToggle}>
          {isEditing ? "Save" : "Edit"}
        </Button>
      </div>
    </div>
  );
}
