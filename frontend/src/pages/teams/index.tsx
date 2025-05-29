import { Card } from "@/components/ui/card";
import { CircleX } from "lucide-react";

export function TeamsPage() {
  return (
    <div className="space-y-4 bg-gray-50">
      <div>
        {/* <h1 className="font-bold text-2xl">My Teams</h1> */}
      </div>
      <div className="h-[620px] mx-4 my-8">
        <Card className="h-full grid place-content-center">
          <div className="space-y-2 text-slate-700">
            <CircleX className="mx-auto size-12" />
            <h1 className="font-semibold text-xl">
              You don&apos;t have any teams, yet!
            </h1>
          </div>
        </Card>
      </div>
    </div>
  );
}
