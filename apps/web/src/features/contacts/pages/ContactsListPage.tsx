import { useState } from "react";
import { Link } from "react-router-dom";
import { useContacts, useDeleteContact } from "../hooks/useContacts";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";

export function ContactsListPage() {
  const [search, setSearch] = useState("");
  const { data, isLoading } = useContacts(search ? { search } : undefined);
  const deleteContact = useDeleteContact();

  const contacts = data?.data ?? [];
  const total = data?.meta?.total ?? 0;

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Contacts <Badge variant="neutral">{total}</Badge></h1>
        <Link to="/contacts/new"><Button>+ Add Contact</Button></Link>
      </div>
      <input
        className="input input-bordered w-full max-w-sm"
        placeholder="Search contacts…"
        value={search}
        onChange={(e) => setSearch(e.target.value)}
      />
      {isLoading ? (
        <div className="flex justify-center py-12"><span className="loading loading-spinner loading-lg" /></div>
      ) : (
        <div className="overflow-x-auto rounded-box border border-base-300">
          <table className="table table-zebra">
            <thead>
              <tr><th>Name</th><th>Email</th><th>Phone</th><th>Title</th><th /></tr>
            </thead>
            <tbody>
              {contacts.length === 0 ? (
                <tr><td colSpan={5} className="text-center text-base-content/50 py-8">No contacts found.</td></tr>
              ) : contacts.map((c) => (
                <tr key={c.id}>
                  <td>
                    <Link to={`/contacts/${c.id}`} className="font-medium link link-hover">
                      {c.firstName} {c.lastName}
                    </Link>
                  </td>
                  <td>{c.email}</td>
                  <td>{c.phone ?? "—"}</td>
                  <td>{c.title ?? "—"}</td>
                  <td className="text-right space-x-2">
                    <Link to={`/contacts/${c.id}/edit`}><Button size="sm" variant="ghost">Edit</Button></Link>
                    <Button size="sm" variant="ghost"
                      onClick={() => confirm("Delete this contact?") && deleteContact.mutate(c.id)}>
                      Delete
                    </Button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
