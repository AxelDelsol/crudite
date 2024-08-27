using Crudite.Models;
using Microsoft.AspNetCore.Mvc;

namespace Crudite.Controllers;

[ApiController]
[Route("[controller]")]
public class TeasController : ControllerBase
{
    private readonly ITeaRepository _teaRepository;

    public TeasController(ITeaRepository teaRepository)
    {
        _teaRepository = teaRepository;
    }

    [HttpGet]
    public async Task<IActionResult> GetTeas()
    {
        return Ok(await _teaRepository.GetTeas());
    }

    [HttpGet("{id}")]
    public async Task<IActionResult> GetTea(int id)
    {
        var tea = await _teaRepository.GetById(id);

        if (tea == null)
        {
            return NotFound();
        }
        return Ok(tea);
    }

    [HttpPost]
    public async Task<IActionResult> CreateTea(Tea teaToCreate)
    {
        var createdTea = await _teaRepository.CreateTea(teaToCreate);
        // GetTea and id are used for the location header
        // createdTea is returned as body
        return CreatedAtAction(nameof(GetTea), new { id = createdTea.Id }, createdTea);
    }

    [HttpDelete("{id}")]
    public async Task<IActionResult> DeleteTea(int id)
    {
        var isDeleted = await _teaRepository.DeleteTea(id);

        return isDeleted ? NoContent() : NotFound();
    }

    [HttpPatch("{id}")]
    public async Task<IActionResult> UpdateQuantity(int id, TeaPatch teaPatch)
    {
        if (id != teaPatch.Id)
        {
            return BadRequest();
        }

        var tea = await _teaRepository.GetById(id);
        if (tea == null)
        {
            return NotFound();
        }

        var patchedTea = await _teaRepository.UpdateQuantity(tea, teaPatch.Quantity);

        return Ok(patchedTea);
    }
}
