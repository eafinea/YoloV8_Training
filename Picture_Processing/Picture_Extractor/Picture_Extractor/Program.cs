using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Picture_Extractor
{
    internal class Program
    {
        static async Task Main(string[] args)
        {
            Console.WriteLine("Please enter the source folder path:");
            string sourceFolder = Console.ReadLine();

            Console.WriteLine("Please enter the destination folder path:");
            string destinationFolder = Console.ReadLine();

            if (string.IsNullOrWhiteSpace(sourceFolder) || string.IsNullOrWhiteSpace(destinationFolder))
            {
                Console.WriteLine("Source and destination folder paths cannot be empty. Exiting...");
                return;
            }

            if (!Directory.Exists(destinationFolder))
            {
                Directory.CreateDirectory(destinationFolder);
            }

            var tasks = Directory.GetDirectories(sourceFolder, "*", SearchOption.AllDirectories)
                .SelectMany(dir => Directory.GetFiles(dir, "*.jpg", SearchOption.TopDirectoryOnly)
                .Select(file => CopyAndRenameFileAsync(file, dir, destinationFolder))).ToArray();

            await Task.WhenAll(tasks);
        }

        static async Task CopyAndRenameFileAsync(string filePath, string originalFolderPath, string destinationFolder)
        {
            string originalFolderName = new DirectoryInfo(originalFolderPath).Name;
            string fileName = Path.GetFileName(filePath);
            string newFileName = $"{originalFolderName}_{fileName}";
            string destinationPath = Path.Combine(destinationFolder, newFileName);

            try
            {
                using (var sourceStream = new FileStream(filePath, FileMode.Open, FileAccess.Read))
                using (var destinationStream = new FileStream(destinationPath, FileMode.Create, FileAccess.Write))
                {
                    await sourceStream.CopyToAsync(destinationStream);
                }

                Console.WriteLine($"File {filePath} copied to {destinationPath}");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error copying file {filePath} to {destinationPath}: {ex.Message}");
            }
        }
    }
}
