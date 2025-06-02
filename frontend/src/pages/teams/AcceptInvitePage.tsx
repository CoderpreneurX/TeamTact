import { useEffect, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Loader2 } from "lucide-react";
import api from "@/utils/api"; // your axios wrapper

export function AcceptInvitePage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const navigate = useNavigate();

  const [loading, setLoading] = useState(true);
  const [success, setSuccess] = useState(false);
  const [message, setMessage] = useState<string>("");

  useEffect(() => {
    if (!searchParams.get("token")) {
      setMessage("Invalid invitation link.");
      setLoading(false);
      return;
    }

    const acceptInvite = async () => {
      try {
        const response = await api.get(`/teams/accept-invite?team_code=${searchParams.get("token")}`);

        if (response.data.success) {
          toast.success("You’ve joined the team successfully!");
          setSuccess(true);
        } else {
          setSuccess(false);
        }

        setMessage(response.data.message);
      } catch {
        setSuccess(false);
        setMessage("Something went wrong while accepting the invite.");
      } finally {
        setLoading(false);
      }
    };

    acceptInvite();
  }, [searchParams]);

  const handleRedirect = () => {
    navigate(success ? "/teams" : "/dashboard");
  };

  return (
    <div className="flex items-center justify-center h-full px-4">
      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle className="text-xl">Accepting Invitation</CardTitle>
        </CardHeader>

        <CardContent className="space-y-4">
          {loading ? (
            <div className="flex items-center justify-center py-8">
              <Loader2 className="w-6 h-6 animate-spin text-muted-foreground" />
              <span className="ml-2 text-muted-foreground">Processing your invite...</span>
            </div>
          ) : (
            <>
              <p className={`text-center ${success ? "text-green-600" : "text-red-500"}`}>
                {message}
              </p>

              <div className="flex justify-center">
                <Button onClick={handleRedirect} className="mt-2">
                  {success ? "Go to Teams" : "Back to Dashboard"}
                </Button>
              </div>
            </>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
