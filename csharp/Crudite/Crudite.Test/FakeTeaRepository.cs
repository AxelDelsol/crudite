using Crudite.Models;

namespace Crudite.Test;
internal class FakeTeaRepository : ITeaRepository
{
    public Dictionary<int, Tea> Teas { get; init; } = new();
    private int _counter = 0;

    public Task<IEnumerable<Tea>> GetTeas()
    {
        return Task.FromResult(Teas.Values.AsEnumerable<Tea>());
    }

    public Task<Tea?> GetById(int id)
    {
        Tea? tea = null;
        bool found = Teas.TryGetValue(id, out tea);

        return Task.FromResult(tea);
    }

    public Task<Tea> CreateTea(Tea tea)
    {

        var newTea = tea with { Id = _counter };
        Teas.Add(_counter, newTea);

        _counter++;
        return Task.FromResult(newTea);
    }

    public Task<bool> DeleteTea(int id) => Task.FromResult(Teas.Remove(id));

    public Task<Tea> UpdateQuantity(Tea tea, int quantity)
    {
        tea.Quantity = quantity;

        return Task.FromResult(tea);
    }
}
