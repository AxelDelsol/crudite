using Crudite.Models;
using Microsoft.EntityFrameworkCore;

namespace Crudite;

public class TeaRepository(TeaContext teaContext) : ITeaRepository
{

    public async Task<IEnumerable<Tea>> GetTeas()
    {
        return await teaContext.Teas.ToListAsync();
    }

    public async Task<Tea?> GetById(int id)
    {
        return await teaContext.Teas.FindAsync(id);
    }

    public async Task<Tea> CreateTea(Tea teaToCreate)
    {
        var teaEntry = teaContext.Teas.Add(teaToCreate);

        await teaContext.SaveChangesAsync();

        return teaEntry.Entity;
    }

    public async Task<bool> DeleteTea(int id)
    {
        var teaToDelete = await GetById(id);

        if (teaToDelete != null)
        {
            teaContext.Teas.Remove(teaToDelete);
            await teaContext.SaveChangesAsync();
            return true;
        }

        return false;
    }

    public async Task<Tea> UpdateQuantity(Tea tea, int quantity)
    {
        tea.Quantity = quantity;
        await teaContext.SaveChangesAsync();

        return tea;
    }
}
