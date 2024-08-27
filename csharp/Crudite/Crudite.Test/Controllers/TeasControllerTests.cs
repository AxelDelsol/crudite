using Crudite.Controllers;
using Crudite.Models;
using Microsoft.AspNetCore.Mvc;

namespace Crudite.Test.Controllers;
public class TeasControllerTests
{
    private readonly TeasController _teasController;
    private readonly FakeTeaRepository _fakeTeaRepository;
    public TeasControllerTests()
    {
        _fakeTeaRepository = new FakeTeaRepository();
        _teasController = new TeasController(_fakeTeaRepository);
    }

    [Theory]
    [InlineData(1)]
    [InlineData(2)]
    async void GetTea_WithExistingId_ReturnsOk(int id)
    {
        _fakeTeaRepository.Teas.Add(1, new() { Id = 1, Name = "Green tea", Quantity = 1 });
        _fakeTeaRepository.Teas.Add(2, new() { Id = 2, Name = "Black tea", Quantity = 2 });

        var result = await _teasController.GetTea(id);

        var okResult = Assert.IsType<OkObjectResult>(result);
        var returnValue = Assert.IsType<Tea>(okResult.Value);
        Assert.Equal(await _fakeTeaRepository.GetById(id), returnValue);
    }

    [Fact]
    async void GetTeas_ReturnsAllTeas()
    {
        var teas = new List<Tea>()
        {
             await _fakeTeaRepository.CreateTea(new Tea() { Name = "Green tea", Quantity = 4 }),
             await _fakeTeaRepository.CreateTea(new Tea() { Name = "Black tea", Quantity = 12 })
        };

        var result = await _teasController.GetTeas();

        var okResult = Assert.IsType<OkObjectResult>(result);
        var returnValue = Assert.IsAssignableFrom<IEnumerable<Tea>>(okResult.Value);
        Assert.Equal(teas.OrderBy(tea => tea.Id), returnValue.OrderBy(tea => tea.Id));

    }

    [Fact]
    async void GetTea_WithUnknownId_ReturnsNotFound()
    {
        int id = 4;

        var result = await _teasController.GetTea(id);

        var notFoundResult = Assert.IsType<NotFoundResult>(result);
    }

    [Fact]
    async void CreateTea_WithValidData_ReturnsCreated()
    {
        var teaToCreate = new Tea() { Name = "New tea", Quantity = 4 };

        var result = await _teasController.CreateTea(teaToCreate);

        var createdAtResult = Assert.IsType<CreatedAtActionResult>(result);
        var createdTea = Assert.IsType<Tea>(createdAtResult.Value);
        Assert.Equal(createdTea, await _fakeTeaRepository.GetById(createdTea.Id));
    }

    [Fact]
    async void DeleteTea_WithExistingTea_ReturnsNoContent()
    {
        var teaToDelete = await _fakeTeaRepository.CreateTea(new Tea() { Name = "Green tea", Quantity = 4 });

        var result = await _teasController.DeleteTea(teaToDelete.Id);

        var noContentResult = Assert.IsType<NoContentResult>(result);
    }

    [Fact]
    async void DeleteTea_WithNonExistingTea_ReturnsNotFound()
    {
        int id = 4;

        var result = await _teasController.DeleteTea(id);

        var notFoundResult = Assert.IsType<NotFoundResult>(result);
    }

    [Fact]
    async void UpdateQuantity_WithExistingTea_ReturnsOK()
    {
        var teaToPatch = await _fakeTeaRepository.CreateTea(new Tea() { Name = "Green tea", Quantity = 4 });

        var result = await _teasController.UpdateQuantity(teaToPatch.Id, new TeaPatch() { Id = teaToPatch.Id, Quantity = 3 });

        var okResult = Assert.IsType<OkObjectResult>(result);
        var patchedTea = Assert.IsType<Tea>(okResult.Value);
        Assert.Equal(teaToPatch with { Quantity = 3 }, patchedTea);
    }

    [Fact]
    async void UpdateQuantity_WithInconsistentIds_ReturnsBadRequest()
    {
        var teaToPatch = await _fakeTeaRepository.CreateTea(new Tea() { Name = "Green tea", Quantity = 4 });

        var result = await _teasController.UpdateQuantity(teaToPatch.Id + 1, new TeaPatch() { Id = teaToPatch.Id, Quantity = 3 });

        var badRequestResult = Assert.IsType<BadRequestResult>(result);
    }

    [Fact]
    async void UpdateQuantity_WithNonExistingTea_ReturnsNotFound()
    {
        var result = await _teasController.UpdateQuantity(4, new TeaPatch() { Id = 4, Quantity = 3 });

        var notFoundResult = Assert.IsType<NotFoundResult>(result);
    }
}
