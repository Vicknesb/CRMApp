import { useNavigate } from "react-router-dom";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { useCreateTicket } from "../hooks/useTickets";
import { Button } from "@/components/ui/Button";

const schema = z.object({
  subject: z.string().min(1),
  description: z.string().optional(),
  channel: z.enum(["EMAIL","PORTAL","PHONE","MANUAL","CHAT"]),
  priority: z.enum(["LOW","MEDIUM","HIGH","CRITICAL"]),
});

type FormValues = z.infer<typeof schema>;

export function TicketFormPage() {
  const navigate = useNavigate();
  const createTicket = useCreateTicket();
  const { register, handleSubmit, formState: { errors } } = useForm<FormValues>({
    resolver: zodResolver(schema),
    defaultValues: { channel: "MANUAL", priority: "MEDIUM" },
  });

  const onSubmit = async (values: FormValues) => {
    await createTicket.mutateAsync(values);
    navigate("/tickets");
  };

  return (
    <div className="max-w-lg">
      <h1 className="text-2xl font-bold mb-6">New Ticket</h1>
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        <div className="form-control">
          <label className="label"><span className="label-text">Subject *</span></label>
          <input className="input input-bordered" {...register("subject")} />
          {errors.subject && <span className="text-error text-sm">{errors.subject.message}</span>}
        </div>
        <div className="form-control">
          <label className="label"><span className="label-text">Description</span></label>
          <textarea className="textarea textarea-bordered" rows={4} {...register("description")} />
        </div>
        <div className="grid grid-cols-2 gap-4">
          <div className="form-control">
            <label className="label"><span className="label-text">Channel</span></label>
            <select className="select select-bordered" {...register("channel")}>
              {["EMAIL","PORTAL","PHONE","MANUAL","CHAT"].map(c => <option key={c} value={c}>{c}</option>)}
            </select>
          </div>
          <div className="form-control">
            <label className="label"><span className="label-text">Priority</span></label>
            <select className="select select-bordered" {...register("priority")}>
              {["LOW","MEDIUM","HIGH","CRITICAL"].map(p => <option key={p} value={p}>{p}</option>)}
            </select>
          </div>
        </div>
        <div className="flex gap-3 pt-2">
          <Button type="submit" disabled={createTicket.isPending}>Create Ticket</Button>
          <Button type="button" variant="ghost" onClick={() => navigate("/tickets")}>Cancel</Button>
        </div>
      </form>
    </div>
  );
}
