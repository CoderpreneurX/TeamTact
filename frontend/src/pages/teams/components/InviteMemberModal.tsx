import { Modal } from "@/components/Modal";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import api from "@/utils/api";
import { API_ROUTES } from "@/utils/constants";
import { zodResolver } from "@hookform/resolvers/zod";
import { UserPlus, Plus, X } from "lucide-react";
import { useForm, useFieldArray } from "react-hook-form";
import { toast } from "sonner";
import * as z from "zod";

const inviteUserSchema = z.object({
  emails: z
    .array(z.string().email("Please enter a valid email address"))
    .min(1, "At least one email is required"),
});

type InviteUserFormValues = z.infer<typeof inviteUserSchema>;

interface InviteUserModalProps {
  teamId: string;
}

export function InviteUserModal({ teamId }: InviteUserModalProps) {
  const {
    register,
    handleSubmit,
    control,
    reset,
    formState: { errors },
  } = useForm<InviteUserFormValues>({
    resolver: zodResolver(inviteUserSchema),
    defaultValues: {
      emails: [""],
    },
  });

  const { fields, append, remove } = useFieldArray({
    control,
    name: "emails",
  });

  const onSubmit = async (values: InviteUserFormValues) => {
    try {
      const response = await api.post(API_ROUTES.TEAMS.INVITE, {
        team_id: teamId,
        emails: values.emails,
      });

      if (response.data?.success === true) {
        reset();
        toast.success(response.data?.message);
      } else {
        toast.error(response.data?.message);
      }
    } catch {
      toast.error("Some Internal Server Error occurred, please try later!");
    }
  };

  const addEmailField = () => {
    append("");
  };

  const removeEmailField = (index: number) => {
    remove(index);
  };

  return (
    <Modal
      trigger={
        <Button className="flex items-center gap-2">
          <UserPlus className="h-4 w-4" />
          Invite Member
        </Button>
      }
      title="Invite new members"
      description="Send invitations to new team members."
      submitButtonText="Send Invitations"
      content={
        <form
          onSubmit={handleSubmit(onSubmit)}
          className="max-h-96 overflow-y-auto"
          id="invite-user-form"
        >
          <div className="grid gap-4">
            <div className="grid gap-2">
              <div className="bg-white py-2 sticky top-0">
                <Label className="">Email Addresses</Label>
              </div>

              <div className="space-y-3">
                {fields.map((field, index) => (
                  <div key={field.id} className="flex gap-2 px-1">
                    <div className="flex-1">
                      <Input
                        type="email"
                        {...register(`emails.${index}`)}
                        placeholder="user@example.com"
                      />
                      {errors.emails?.[index] && (
                        <p className="text-sm text-red-500 mt-1">
                          {errors.emails[index]?.message}
                        </p>
                      )}
                    </div>

                    {fields.length > 1 && (
                      <Button
                        type="button"
                        variant="outline"
                        onClick={() => removeEmailField(index)}
                        className="flex items-center justify-center text-red-500 hover:text-red-700 hover:bg-red-50"
                      >
                        <X className="h-4 w-4" />
                      </Button>
                    )}
                  </div>
                ))}
              </div>

              <div className="p-1 bg-white sticky bottom-0">
                <Button
                  type="button"
                  variant="outline"
                  size="sm"
                  onClick={addEmailField}
                  className="flex items-center gap-1 w-fit"
                >
                  <Plus className="h-3 w-3" />
                  Add Email
                </Button>

                {errors.emails && (
                  <p className="text-sm text-red-500 mt-1">
                    {errors.emails.message}
                  </p>
                )}
              </div>
            </div>
          </div>
        </form>
      }
      formId="invite-user-form"
    />
  );
}
