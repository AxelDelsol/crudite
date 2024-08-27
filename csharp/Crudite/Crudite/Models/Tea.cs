
namespace Crudite.Models;

public record Tea : IEquatable<Tea?>
{
    public int Id { get; set; }
    public string Name { get; set; } = null!;
    public int Quantity { get; set; }
}

public class TeaPatch
{
    public int Id { get; set; }
    public int Quantity { get; set; }
}
