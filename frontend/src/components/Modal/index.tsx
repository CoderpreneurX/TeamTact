import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { useState, type ReactNode } from "react";

interface ModalProps {
  trigger: ReactNode;
  title: string;
  description?: string;
  content: ReactNode;
  submitButtonText?: string | ReactNode;
  cancelButtonText?: string;
  onSubmit?: () => void;
  onCancel?: () => void;
  formId?: string;
}

export function Modal({
  title,
  trigger,
  description,
  content,
  cancelButtonText,
  submitButtonText = "Save",
  onSubmit = () => {},
  onCancel,
  formId,
}: ModalProps) {
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const handleSubmit = async () => {
    setIsLoading(true);
    try {
      await onSubmit();
    } finally {
      setIsLoading(false);
    }
  };

  const renderSubmitButtonContent = () => {
    if (isLoading) {
      return (
        <span className="flex items-center">
          <div className="border-2 border-white border-r-transparent animate-spin h-4 w-4 mr-2 rounded-full" />
          Saving...
        </span>
      );
    }

    return submitButtonText;
  };

  return (
    <Dialog>
      <DialogTrigger asChild>{trigger}</DialogTrigger>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>{title}</DialogTitle>
          {description && <DialogDescription>{description}</DialogDescription>}
        </DialogHeader>
        {content}
        <DialogFooter>
          <DialogClose asChild>
            <Button
              variant="outline"
              onClick={onCancel}
              disabled={isLoading}
            >
              {cancelButtonText ?? "Cancel"}
            </Button>
          </DialogClose>
          <Button
            type="submit"
            form={formId}
            onClick={handleSubmit}
            disabled={isLoading}
          >
            {renderSubmitButtonContent()}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
