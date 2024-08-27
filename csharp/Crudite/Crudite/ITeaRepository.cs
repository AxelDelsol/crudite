using Crudite.Models;

namespace Crudite;

public interface ITeaRepository
{
    Task<IEnumerable<Tea>> GetTeas();
    Task<Tea?> GetById(int id);
    Task<Tea> CreateTea(Tea teaToCreate);
    Task<bool> DeleteTea(int id);
    Task<Tea> UpdateQuantity(Tea tea, int quantity);
}