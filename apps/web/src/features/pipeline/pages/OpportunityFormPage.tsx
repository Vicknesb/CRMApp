import { useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { useOpportunity, useCreateOpportunity, useUpdateOpportunity } from "../hooks/usePipeline";
import { Button } from "@/components/ui/Button";

const schema = z.object({
  title: z.string().min(1),
  value: z.coerce.number().min(0),
  stageId: z.string().min(1, "Stage is required"),
  accountId: z.string().optional(),
  contactId: z.string().optional(),
  expectedCloseDate: z.string().optional(),
});

type FormValues = z.infer<typeof schema>;

export function OpportunityFormPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const isEdit = !!id;
  const { data: opp } = useOpportunity(id ?? "");
  const createOpp = useCreateOpportunity();
  const updateOpp = useUpdateOpportunity();

  const { register, handleSubmit, reset, formState: { errors } } = useForm<FormValues>({
    resolver: zodResolver(schema),
  });

  useEffect(() => {
    if (opp) reset(opp);
  }, [opp, reset]);

  const onSubmit = async (values: FormValues) => {
    if (isEdit) {
      await updateOpp.mutateAsync({ id: id!, body: values });
    } else {
      await createOpp.mutateAsync(values);
    }
    navigate("/pipeline");
  };

  return (
    <div className="max-w-lg">
      <h1 className="text-2xl font-bold mb-6">{isEdit ? "Edit" : "New"} Opportunity</h1>
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        <div className="form-control">
          <label className="label"><span className="label-text">Title *</span></label>
          <input className="input input-bordered" {...register("title")} />
          {errors.title && <span className="text-error text-sm">{errors.title.message}</span>}
        </div>
        <div className="grid grid-cols-2 gap-4">
          <div className="form-control">
            <label className="label"><span className="label-text">Value (₹) *</span></label>
            <input className="input input-bordered" type="number" step="0.01" {...register("value")} />
            {errors.value && <span className="text-error text-sm">{errors.value.message}</span>}
          </div>
          <div className="form-control">
            <label className="label"><span className="label-text">Stage ID *</span></label>
            <input className="input input-bordered" {...register("stageId")} />
            {errors.stageId && <span className="text-error text-sm">{errors.stageId.message}</span>}
          </div>
        </div>
        <div className="form-control">
          <label className="label"><span className="label-text">Expected Close Date</span></label>
          <input className="input input-bordered" type="date" {...register("expectedCloseDate")} />
        </div>
        <div className="flex gap-3 pt-2">
          <Button type="submit" disabled={createOpp.isPending || updateOpp.isPending}>
            {isEdit ? "Save Changes" : "Create Opportunity"}
          </Button>
          <Button type="button" variant="ghost" onClick={() => navigate("/pipeline")}>Cancel</Button>
        </div>
      </form>
    </div>
  );
}
